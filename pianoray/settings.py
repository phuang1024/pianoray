from typing import Any, Mapping


class Settings:
    """
    Settings.
    """

    _data: Mapping[str, Any]

    def __init__(self, data: Mapping[str, Any]) -> None:
        object.__setattr__(self, "_data", {})
        for key in data:
            obj = data[key]
            if isinstance(obj, dict):
                obj = Settings(obj)
            self._data[key] = obj

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Settings object has no attribute {name}")

    def __setattr__(self, name: str, value: Any) -> None:
        self._data[name] = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Settings):
            return False
        return self._data == other._data

    def _merge(self, other: "Settings") -> None:
        """
        Merge other settings with self, keeping self if conflict.
        """
        for key in other:
            obj = getattr(other, key)
            if not hasattr(self, key):
                self._data[key] = obj
            else:
                if isinstance(obj, Settings):
                    getattr(self, key)._merge(obj)

    def _json(self) -> Mapping[str, Any]:
        ret = {}
        for key in self._data:
            obj = self._data[key]
            if isinstance(obj, Settings):
                obj = obj._json()
            ret[key] = obj

        return ret
