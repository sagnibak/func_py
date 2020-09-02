from funcy import putStrLn, getLine

# IO monad demo
(
    putStrLn("What is your name, bro?")
        .chain(lambda _: getLine())
        .chain(lambda name: putStrLn("Hello, " + name + "!"))
        .chain(lambda _: putStrLn("\nHow old are you right now?"))
        .chain(lambda _: getLine())
        .map(lambda age_str: int(age_str))
        .map(lambda age: age + 1)
        .chain(lambda new_age: putStrLn(f"At this time next year, you will be {new_age} years old."))
)