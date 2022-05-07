from typing import Any, Mapping


class Accessor:
    """
    Can access stuff with getattr.
    """
    _attrs: Mapping[str, Any]

    def __init__(self, attrs: Mapping[str, Any]):
        """
        All dicts in attrs are replaced with an Accessor object.
        """
        self._attrs = {}
        for k, v in attrs.items():
            if isinstance(v, dict):
                v = Accessor(v)
            self._attrs[k] = v

    def __getattr__(self, name: str) -> Any:
        return self._attrs[name]

    def _as_dict(self) -> Mapping[str, Any]:
        ret = {}
        for k, v in self._attrs.items():
            if isinstance(v, Accessor):
                v = v._as_dict()
            ret[k] = v

        return ret
