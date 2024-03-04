# Base Activity v2
class BaseActivityV2:

    def __init__(self, context):
        # type: (dict) -> None
        self.context = context
        pass

    def update(self, code, payload):
        # type: (int, dict) -> None
        res = self._update(code, payload)
        if res:
            self._render(code, payload)

    def _render(self, code, payload):
        # type: (int, dict) -> None
        pass

    def _update(self, code, payload):
        # type: (int, dict) -> bool
        return True
