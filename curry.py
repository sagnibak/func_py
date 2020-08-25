from typing import *

ReturnType = TypeVar("ReturnType")


def curry(num_args: int) -> Callable[[Callable[..., ReturnType]], Partial[ReturnType]]:
    """Curries the decorated function. Instead of having to provide all arguments
    at once, they can be provided one or a few at a time. Once at least `num_args`
    arguments are provided, the wrapped function will be called. The doctests below
    best illustrate its use.

    >>> @curry(num_args=3)
    ... def add(a, b, c):
    ...     return a + b + c
    >>> add5 = add(5)
    >>> add7 = add5(2)

    You can still call the function without currying.
    >>> add(1, 2, 3)
    6

    This is not "real" currying, but it allows passing more complex state,
    so I'd say this is in the spirit of currying and should be legal.
    >>> add5(4, 3)
    12
    >>> add(1)(2, 3)
    6
    >>> add(1, 2)(3)
    6

    Strict currying:
    >>> add5(4)(3)
    12
    >>> add7(2)
    9
    >>> add(1)(2)(3)
    6

    It is okay to have some default arguments. Notice that the wrapped function
    `make_email` takes up to three arguments, but gets called when at least two
    are provided.
    >>> @curry(num_args=2)
    ... def make_email(username, domain, separator="@"):
    ...     return username + separator + domain
    >>> make_gmail = make_email(domain="gmail.com")
    >>> make_gmail("haskell")
    'haskell@gmail.com'
    >>> make_gmail(username="curry")
    'curry@gmail.com'
    >>> make_gmail("curry", separator=">>=")
    'curry>>=gmail.com'
    >>> make_email("haskell", "curry.com")
    'haskell@curry.com'
    >>> make_email("haskell")("curry.com", ">>=")
    'haskell>>=curry.com'

    Parameters
    ----------
    num_args    number of arguments to wait for before evaluating wrapped function

    Returns
    -------
    a decorator that curries a function
    """

    def currier(fn: Callable[..., ReturnType]):
        return Partial(num_args, fn)

    return currier


class Partial(Generic[ReturnType]):
    """Represents a partial function application. `fn` is the function being
    wrapped, and the args and kwargs are the saved ones from previous calls.
    """

    def __init__(
        self, num_args: int, fn: Callable[..., ReturnType], *args, **kwargs
    ) -> None:
        self.num_args = num_args
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs) -> Union[Partial[ReturnType], ReturnType]:
        child_kwargs = self.kwargs.copy()
        child_kwargs.update(kwargs)
        num_args = len(self.args + args) + len(child_kwargs)
        if num_args >= self.num_args:
            return self.fn(*(self.args + args), **child_kwargs)
        else:
            return Partial(self.num_args, self.fn, *(self.args + args), **child_kwargs)

    def __repr__(self):
        return f"Partial({self.fn}, args={self.args}, kwargs={self.kwargs})"
