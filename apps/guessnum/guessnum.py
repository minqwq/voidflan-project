import random
import sys

print("Guess number v0.1R2 by minqwq and Copilot")
print("1: max20\n2: max60\n3: max100\n4: max200\n5: max400\n6: max800\n7: max1600")

diffs = ("1", "2", "3", "4", "5", "6", "7")
numRange = (20, 60, 100, 200, 400, 800, 1600)

diff = input("Select a difficulty: ")
if diff not in diffs or diff == "":
    sys.exit()

numRangeMax = dict(zip(diffs, numRange))[diff]


randomResult = random.randint(0, numRangeMax)
looping = True

print("HELP:\nexit:exit\nType some number to guess")

while looping:
    correctNum = randomResult
    guess = input("INPUT AREA > ")
    ln = len(guess)
    if ln and guess == 'exit':
        sys.exit()
    if ln and guess.isnumeric():
        guessing = int(guess)  # Convert input to an integer
        
        if guessing > correctNum:
            print("Number too high")
        elif guessing < correctNum:
            print("Number too low")
        elif guessing == correctNum:
            print("You win~")
            sys.exit()
