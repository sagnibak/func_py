main = do
    putStrLn "What is your name, bro?"
    name <- getLine
    putStrLn ("Hello, " ++ name ++ "!")
    putStrLn "\nHow old are you right now?"
    age_str <- getLine
    let new_age = show ((read age_str :: Int) + 1)
    putStrLn ("At this time next year, you will be " ++ new_age ++ " years old.")
