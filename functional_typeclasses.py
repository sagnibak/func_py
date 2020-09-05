from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from collections.abc import Iterable
from functools import reduce
from typing import Any, Callable, Generic, Iterator, TypeVar
from typing_extensions import Protocol

__all__ = [
    "Foldable",
    "Functor",
    "Monad",
    "Monoid",
    "Semigroup",
    "Show",
    "Unwrappable",
]

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

class Show:
    def __init__(self) -> None:
        self._contents: Any  # to make the type checker happy
    
    def __repr__(self) -> str:
        className = self.__class__.__name__
        if hasattr(self, "_contents"):
            return f"{className}({repr(self._contents)})"
        else:
            return f"{className}()"

