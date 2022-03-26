"""
Author: Thomas Janssen
Date Created: 23/03/2022

Solve Wordles in English and Dutch.

Example: 
solution =  store 
guess #1 =  arose
feedback =  _rOsE
"""

import csv
from colorama import Fore, Style, Back

# Read CSV file with 5-letter words in chosen language
language = input('Please choose a languague: EN (default) or NL: ') or 'EN' # Supports 'NL' or 'EN'
match language:
    case 'NL':
        file = 'Dutch-5-letter-words-woordle.csv'
    case 'EN':
        file = 'English-5-letter-words-wordle.csv'
    case _:
        file = 'English-5-letter-words-wordle.csv'

with open(file, 'r') as f:
    reader = csv.reader(f)
    words = f.read().split(',')

# Start game loop
while True:

    # Input the guessed word and the green and yellow letters, and validate the input
    while True:
        guess = input('Please input your guess: ') # only necessary for removing black letters
        feedback = input('Please indicate green (capital) letters, yellow (small) letters, and other letter spots with "_": ') # __aiR

        if len(guess) != 5:
            print('The word must have 5 characters!')
            continue
        elif len(feedback) != 5:
            print('There must be 5 characters in the feedback!')
            continue
        else:
            print('Valid input: ', end='')
            break

    # Based on the feedback, create list of black, yellow and green letters and their locations
    yellow_letters = {}
    green_letters = {}
    black_letters = {}
    for i, char in enumerate(feedback):
        if char == '_':
            black_letters[i] = guess[i]
            print(f'{Back.BLACK}{Fore.WHITE} {char.upper()} ', end='')
        elif char.isupper():
            green_letters[i] = char.lower()
            print(f'{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} {char.upper()} ', end='')
        else:
            yellow_letters[i] = char
            print(f'{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} {char.upper()} ', end='')

    print(Style.RESET_ALL)
    # print(f'Green letters: {green_letters}')  # {2: 'o', 4: 'e'}
    # print(f'Yellow letters: {yellow_letters}')  # {1: 'r'}
    # print(f'Black letters: {black_letters}')


    # Match green letters
    possible_words_green = []
    for word in words:   
        if all(green_letters[i] == word[i] for i in green_letters.keys()):
            possible_words_green.append(word)

    # Match yellow letters
    possible_words_yellow = []
    for word in possible_words_green:
        if all(yellow_letter in word for yellow_letter in yellow_letters.values()):
            possible_words_yellow.append(word)

    # Remove words with black letters
    possible_words_black = []
    for word in possible_words_yellow:
        if not any(black_letter in word for black_letter in black_letters.values()):
            possible_words_black.append(word)

    # Remove words with letters on the same location as yellow letters
    possible_words = []
    for word in possible_words_black:
        if not any(yellow_letters[i] == word[i] for i in yellow_letters.keys()):
            possible_words.append(word)

    # Start over but only with possible words
    print(f'{len(possible_words)} possible words: {sorted(possible_words)}')
    words = possible_words
    if len(words) == 1:
        print('Congrats, you sneaky Wordle cheater!')
        break