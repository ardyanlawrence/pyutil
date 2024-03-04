try:
    # pip >=20
    from pip._internal.req import parse_requirements
    from pip._internal.network.session import PipSession
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.req import parse_requirements
        from pip._internal.download import PipSession
    except ImportError:
        # pip <= 9.0.3
        from pip.req import parse_requirements
        from pip.download import PipSession
from setuptools import find_packages, setup


def parse_install_requires(requirements):
    try:
        install_reqs = parse_requirements(requirements, session=PipSession())
        return [str(r.requirement) for r in install_reqs]
    except AttributeError:
        with open(requirements) as f:
            return [r.strip('\n') for r in f if r.strip('\n') and not r.startswith('#')]


# Parse requirements.txt to get the list of dependencies
_install_requires = parse_install_requires('requirements.txt')


# Read version from file
def read_version():
    from re import findall
    py = open('src/pyutil/__init__.py').read()
    metadata = dict(findall("__([a-z]+)__ = '([^']+)'", py))
    return metadata['version']


setup(
    name='pyutil-base',
    version=read_version(),
    license='unlicensed',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=_install_requires,
    zip_safe=True
)
