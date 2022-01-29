from ctypes.wintypes import WORD
import sys
import random
from colorama import Fore, Back, Style

NUM_ROUNDS = 6
WORD_LENGTH = 5

CORRECT = 2
PARTIAL = 1
WRONG = 0

words = []
n = 0

#Main function to read in words list and begin the game
def main():
    with open("words.txt") as f:
        contents = f.read()
        global words
        words = contents.split("\n")
    global n
    n = len(words)
    game()

#Start running the game
def game():
    target = choose_target()
    for round in range(NUM_ROUNDS):
        guess = get_valid_guess()
        if check_guess(guess, target):
            win()
    lose(target)

#Randomly choose a target word for the current game
def choose_target():
    index = random.randint(0, n)
    return words[index]

#Get the player's next guess
def get_valid_guess():
    guess = ""
    while len(guess) != WORD_LENGTH or guess not in words:
        guess = input().lower()
        #cursor up one line
        sys.stdout.write('\x1b[1A')
        #delete last line
        sys.stdout.write('\x1b[2K')
    return guess

#Check how close the current guess is to the target
def check_guess(guess, target):
    correct_guess = True
    accuracy = [WRONG]*WORD_LENGTH
    letters_remaining = {}
    for i in range(WORD_LENGTH):
        if guess[i] == target[i]:
            accuracy[i] = CORRECT
        else:
            correct_guess = False
            if target[i] in letters_remaining:
                letters_remaining[target[i]] += 1
            else:
                letters_remaining[target[i]] = 1
    for i in range(WORD_LENGTH):
        if guess[i] != target[i] and guess[i] in letters_remaining:
            accuracy[i] = PARTIAL
            if letters_remaining[guess[i]] > 1:
                letters_remaining[guess[i]] -= 1
            else:
                letters_remaining.pop(guess[i])
    print_guess(guess, accuracy)
    return correct_guess
    
#Print the user's guess with appropriate colors
def print_guess(guess, accuracy):
    for i in range(WORD_LENGTH):
        if accuracy[i] == CORRECT:
            print(Fore.GREEN + guess[i], end="")
        elif accuracy[i] == PARTIAL:
            print(Fore.YELLOW + guess[i], end="")
        else:
            print(Fore.WHITE + guess[i], end="")
    print(Style.RESET_ALL)

def win():
    print("Correct Guess, you win!")
    exit()

def lose(target):
    print("You ran out of guesses!  The correct word was \"" + target + "\"")
    exit()

if __name__ == "__main__":
    main() 