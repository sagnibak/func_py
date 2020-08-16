from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar


ReturnType = TypeVar("ReturnType")


@dataclass
class Thunk(Generic[ReturnType]):
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    return_val: Optional[ReturnType] = None


def tco(fn: Callable[..., Thunk[ReturnType]]) -> Callable[..., ReturnType]:
    """Annotating a tail-recursive function `fn` with this decorator allows
    tail-call optimization. When the function wants to make a recursive call,
    it returns a Thunk with a tuple of positional arguments, a dictionary of
    keyword arguments, and a None return_val. When the function does not want
    to make a tail call but simply wants to return, it should return a Thunk
    with a return_val of type ReturnType.

    Parameters
    ----------
    fn  tail-recursive function in need of optimization

    Returns
    -------
    tail call optimized version of function `fn`
    """

    def inner(*args, **kwargs) -> ReturnType:
        result = fn(*args, **kwargs)
        while result.return_val is None:
            result = fn(*result.args, **result.kwargs)
        return result.return_val

    return inner


if __name__ == "__main__":
    # examples
    @tco
    def factorial(n: int, acc: int = 1) -> Thunk[int]:
        if n == 0:
            return Thunk(return_val=acc)
        else:
            return Thunk((n - 1, n * acc))

    actual = list(map(factorial, range(10)))
    expected = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
    assert actual == expected
    assert factorial(10000) is not None

    @tco
    def fibonacci(n: int, cur: int = 1, nxt: int = 1) -> Thunk[int]:
        if n == 0:
            return Thunk(return_val=cur)
        else:
            return Thunk((n - 1, nxt, cur + nxt))

    actual = list(map(fibonacci, range(10)))
    expected = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    assert actual == expected
    assert fibonacci(10000) is not None
