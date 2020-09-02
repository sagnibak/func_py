from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from functools import reduce
from typing import Callable, Generic, Iterator, TypeVar
from typing_extensions import Protocol

A_co = TypeVar("A_co", covariant=True)
B = TypeVar("B")
class Functor(Protocol, Generic[A_co]):
    def map(self: Functor[A_co], fn: Callable[[A_co,], B]) -> Functor[B]:
        ...

class Semigroup(Protocol):
    def combine(self: Semigroup, other: Semigroup) -> Semigroup:
        ...

class Monoid(Semigroup, Protocol):
    @classmethod
    def empty(cls) -> Monoid:
        ...

A = TypeVar("A")
class Monad(Functor, Protocol, Generic[A]):
    @classmethod
    def of(cls, *args: A) -> Monad[A]:
        ...
    
    def chain(self: Monad[A], fn: Callable[[A,], Monad[B]]) -> Monad[B]:
        ...

Acc = TypeVar("Acc")
class Foldable(Functor, Protocol, Generic[A_co]):
    def foldl(self: Foldable[A_co], fn: Callable[[Acc, A_co], Acc], initial: Acc) -> Acc:
        ...

    def foldr(self: Foldable[A_co], fn: Callable[[A_co, Acc], Acc], initial: Acc) -> Acc:
        ...

class Unwrappable(Protocol, Generic[A_co]):
    def unwrap(self: Unwrappable[A_co]) -> A_co:
        ...

class Box(Generic[A_co]):
    def __init__(self, contents) -> None:
        self._contents = contents

    def map(self: Box[A_co], fn: Callable[[A_co,], B]) -> Box[B]:
        return Box.of(fn(self.unwrap()))

    @classmethod
    def of(cls, *args: A) -> Box[A]:
        return Box(*args)
    
    def chain(self, fn):
        return fn(self.unwrap())
    
    def unwrap(self: Box[A_co]) -> A_co:
        return self._contents

class List(Generic[A_co]):
    def __init__(self, *contents) -> None:
        self._contents = list(contents)
    
    def map(self: List[A_co], fn: Callable[[A_co,], B]) -> List[B]:
        return List.of(*map(fn, self._contents))

    def combine(self, other):
        return List.of(*(self._contents + other._contents))
    
    @classmethod
    def empty(cls) -> List[A_co]:
        return List.of()
    
    @classmethod
    def of(cls, *args: A) -> List[A]:
        return List(*args)
    
    def chain(self, fn):
        return List.of(*(b for sublist in map(fn, self._contents) for b in sublist))
    
    def foldl(self: List[A_co], fn: Callable[[Acc, A_co], Acc], initial: Acc) -> Acc:
        return reduce(fn, self._contents, initial)

    def foldr(self: List[A_co], fn: Callable[[A_co, Acc], Acc], initial: Acc) -> Acc:
        return reduce(lambda acc, a: fn(a, acc), reversed(self._contents), initial)

    def __iter__(self) -> Iterator[A_co]:
        return iter(self._contents)

class Option(ABC, Generic[A]):
    @abstractmethod
    def map(self, fn):
        raise NotImplementedError

    @abstractclassmethod
    def of(cls, *args: A):
        raise NotImplementedError
    
    @abstractmethod
    def chain(self, fn):
        raise NotImplementedError
    
    @abstractmethod
    def unwrap(self):
        raise NotImplementedError

class Some(Option, Generic[A]):
    def __init__(self, contents):
        self._contents = contents

    def map(self, fn):
        return Some.of(fn(self.unwrap()))

    @classmethod
    def of(cls, *args: A):
        return Some(*args)
    
    def chain(self, fn):
        return fn(self.unwrap())
    
    def unwrap(self):
        return self._contents

class Nothing(Option, Generic[A]):
    def map(self, fn):
        return Nothing()

    @classmethod
    def of(cls, *args: A):
        raise TypeError("Cannot put anything inside a `Nothing`.")
    
    def chain(self, fn):
        return Nothing()
    
    def unwrap(self):
        raise TypeError("Cannot unwrap a `Nothing` since it contains...nothing!")

class Result(ABC, Generic[A]):
    def __init__(self, contents):
        self._contents = contents

    @abstractmethod
    def map(self, fn):
        raise NotImplementedError

    @classmethod
    def of(cls, *args: A):
        return cls(*args)
    
    @abstractmethod
    def chain(self, fn):
        raise NotImplementedError
    
class Ok(Result, Generic[A]):
    def map(self: Ok[A], fn: Callable[[A,], B]) -> Ok[B]:
        return Ok.of(fn(self.unwrap()))

    def chain(self: Ok[A], fn: Callable[[A,], Result[B]]) -> Result[B]:
        return fn(self.unwrap())
    
    def unwrap(self: Ok[A]) -> A:
        return self._contents

class Err(Result, Generic[A]):
    def map(self: Err[A], fn: Callable[[A,], B]) -> Err[A]:
        return self

    def chain(self: Err[A], fn: Callable[[A,], Result[B]]) -> Err[A]:
        return self
    
    def unwrap(self: Err[A]) -> A:
        raise Exception(self._contents)

class IO(Generic[A]):
    def __init__(self, contents: A) -> None:
        self._contents = contents
    
    def map(self: IO[A], fn: Callable[[A,], B]) -> IO[B]:
        return IO.of(fn(self._contents))
    
    @classmethod
    def of(cls, *args: A):
        return IO(*args)
    
    def chain(self: IO[A], fn: Callable[[A,], IO[B]]) -> IO[B]:
        return fn(self._contents)


def getLine() -> IO[str]:
    return IO.of(input())

def putStrLn(s: str) -> IO[None]:
    print(s)
    return IO.of(None)


if __name__ == "__main__":
    # these lines should typecheck
    a: Monad[int] = List.of(1, 2, 3)
    b: Box[str] = Box.of("foo")
    c: Monad[int] = Box.of(b.map(lambda s: len(s)).unwrap())
    d: Unwrappable[int] = Box.of(b.map(lambda s: len(s)).unwrap())
    e: Semigroup = List.of(1, 2, 4)
    f: Monoid = List.of(1, 2, 4)
    g: Monad[int] = Some.of(4)
    h: Functor[int] = g
    i: Monad[int] = Nothing()
    j: Monad[str] = IO.of("foo")
    k: Functor[str] = j
    l: Monad[str] = Ok.of("This should be a Monad of a string")
    m: Unwrappable[str] = Ok.of("This should be unwrappable")
    n: Monad[str] = Err.of(ValueError("Explodes on unwrap!"))
    o: Unwrappable[str] = Err.of(ValueError("Explodes on unwrap!"))
