import functools
from typing import Callable
from dataclasses import dataclass

type Result[T, E] = Ok | Err


@dataclass
class Ok:
    value: object

    def map(self, f: Callable) -> "Ok | Err":
        return Ok(f(self.value))

    def bind(self, f: Callable) -> "Ok | Err":
        return f(self.value)

    def unwrap_or(self, default: object) -> object:
        return self.value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False


@dataclass
class Err:
    error: Exception

    def map(self, f: Callable) -> "Err":
        return self

    def bind(self, f: Callable) -> "Err":
        return self

    def unwrap_or(self, default: object) -> object:
        return default

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True


def result_wrap(f: Callable) -> Callable:
    @functools.wraps(f)
    def wrapper(*args, **kwargs) -> Ok | Err:
        try:
            result = f(*args, **kwargs)
            if isinstance(result, (Ok, Err)):
                return result
            return Ok(result)
        except Exception as e:
            return Err(e)
    return wrapper


def async_result_wrap(f: Callable) -> Callable:
    @functools.wraps(f)
    async def wrapper(*args, **kwargs) -> Ok | Err:
        try:
            result = await f(*args, **kwargs)
            if isinstance(result, (Ok, Err)):
                return result
            return Ok(result)
        except Exception as e:
            return Err(e)
    return wrapper
