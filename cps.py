from typing import *
from dataclasses import dataclass


def safe_floor(a: int, b: int) -> Optional[int]:
    if b == 0:
        print("Division by zero")
        return None
    else:
        return a // b


def safe_floor2(a: int, b: int):
    def inner(ok, err):
        if b == 0:
            return err("Division by zero")
        else:
            return ok(a // b)

    return inner


T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Ok(Generic[T]):
    val: T


@dataclass
class Err(Generic[E]):
    err: E


Result = Union[Ok[T], Err[E]]


def cps_result(fn: Callable[..., Result[T, E]]):
    def inner(*args, **kwargs) -> Optional[T]:
        result = fn(*args, **kwargs)
        if isinstance(result, Ok):
            return result.val
        else:
            print(result.err)
            return None

    return inner


@cps_result
def safe_floor3(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("Division by zero")
    else:
        return Ok(a // b)


if __name__ == "__main__":
    identity = lambda x: x
    assert 2 == safe_floor(6, 3)
    assert 2 == safe_floor2(6, 3)(identity, print)
    assert 2 == safe_floor3(6, 3)
    assert safe_floor(6, 0) is None
    assert safe_floor2(6, 0)(identity, print) is None
    assert safe_floor3(6, 0) is None
