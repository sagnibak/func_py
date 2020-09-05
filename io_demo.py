from typing import Tuple
from fio import RealWorld, getLine, putStrLn

# IO monad demo
def main(realWorld: RealWorld) -> Tuple[None, RealWorld]:
    return (
        putStrLn("What is your name, bro?")
            .chain(lambda _: getLine())
            .chain(lambda name: putStrLn("Hello, " + name + "!"))
            .chain(lambda _: putStrLn("\nHow old are you right now?"))
            .chain(lambda _: getLine())
            .map(lambda age_str: int(age_str))
            .map(lambda age: age + 1)
            .chain(lambda new_age: putStrLn(f"At this time next year, you will be {new_age} years old."))
            .__call__(realWorld)
    )

if __name__ == "__main__":
    realWorld = RealWorld()
    done, potentiallyChangedWorld = main(realWorld)
