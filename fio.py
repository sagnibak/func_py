from __future__ import annotations
from abc import ABC, abstractclassmethod, abstractmethod
from collections.abc import Iterable
from functools import reduce
from typing import Any, Callable, Generic, Iterator, Tuple, TypeVar
from typing_extensions import Protocol

from functional_typeclasses import *

A = TypeVar("A")
A_co = TypeVar("A_co", covariant=True)
B = TypeVar("B")
Acc = TypeVar("Acc")

class RealWorld:
    pass

class IO(Show, Generic[A_co]):
    def __init__(self, world: Any, contents: A_co) -> None:
        self.world = world
        self._contents = contents
    
    def __call__(self, realWorld: RealWorld) -> Tuple[A, RealWorld]:
        return self._contents, realWorld
    
    def map(self: IO[A_co], fn: Callable[[A_co,], B]) -> IO[B]:
        return IO.of(fn(self._contents))
    
    @classmethod
    def of(cls, *args: A):
        return IO(0, *args)
    
    def chain(self: IO[A_co], fn: Callable[[A_co,], IO[B]]) -> IO[B]:
        return fn(self._contents)


def getLine() -> IO[str]:
    return IO.of(input())

def putStrLn(s: str) -> IO[None]:
    print(s)
    return IO.of(None)


def readFile(fname: str) -> IO[str]:
    with open(fname, "r") as f:
        lines = f.read()
    return IO.of(lines)

def writeFile(fname: str, contents: str) -> IO[None]:
    with open(fname, "w") as f:
        f.write(contents)
    return IO.of(None)


if __name__ == "__main__":
    j: Monad[str] = IO.of("foo")
    k: Functor[str] = j
    l: Monad[Any] = j  # covariance!
