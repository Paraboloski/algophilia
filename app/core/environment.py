import os
from typing import Any, Callable, cast
from app.core.exception import EnvError
from app.core.result import Ok, Err, Result

class Env:
    def __init__(self, variable: str = ""):
        self._variable = f"{variable.rstrip('_')}_" if variable else ""

    def _key(self, name: str) -> str:
        return f"{self._variable}{name.upper()}"

    def _get(self, name: str) -> Result[str]:
        value = os.getenv(self._key(name))
        if value is None:
            return Err(EnvError(f"Variabile mancante: '{self._key(name)}'"))
        return Ok(value)

    def _cast(self, name: str, function: Callable[[str], Any]) -> Result[Any]:
        def safe(v: str) -> Any:
            try:
                return function(v)
            except (ValueError, TypeError):
                raise EnvError(f"Impossibile convertire '{self._key(name)}={v!r}' in {function.__name__}")

        return cast(Result[Any], self._get(name).bind(lambda v: Ok(safe(v))))

    def string(self, name: str) -> Result[str]:
        return self._get(name)

    def integer(self, name: str) -> Result[int]:
        return cast(Result[int], self._cast(name, int))

    def number(self, name: str) -> Result[float]:
        return cast(Result[float], self._cast(name, float))

    def boolean(self, name: str) -> Result[bool]:
        def parse(v: str) -> bool:
            if v.lower() in {"1", "true", "yes", "on"}:
                return True
            if v.lower() in {"0", "false", "no", "off"}:
                return False
            raise EnvError(f"Valore non valido per '{self._key(name)}': '{v}'")

        return cast(Result[bool], self._get(name).bind(lambda v: Ok(parse(v))))
