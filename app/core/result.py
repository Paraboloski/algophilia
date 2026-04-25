from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Callable, Generic, Union, Never

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=BaseException)

@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    def bind(self, function: Callable[[T], Result[U]]) -> Result[U]:
        try:
            return function(self.value)
        except Exception as e:
            return Err(e)

    def map(self, function: Callable[[T], U]) -> Result[U]:
        return self.bind(lambda x: Ok(function(x)))

    def unwrap(self) -> T:
        return self.value

    def is_ok(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E

    def bind(self, function: Callable) -> Result[Never]:
        return self

    def map(self, function: Callable) -> Result[Never]:
        return self

    def unwrap(self) -> Never:
        raise self.error

    def is_ok(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"Err({self.error!r})"


Result = Union[Ok[T], Err]

def result(function: Callable[..., T]) -> Callable[..., Result[T]]:
    def wrapper(*args, **kwargs) -> Result[T]:
        try:
            return Ok(function(*args, **kwargs))
        except Exception as e:
            return Err(e)
    return wrapper
