#!/usr/bin/env python3

import random


def main():
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")
    number = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            guess = int(input("Take a guess: "))
        except ValueError:
            print("Please enter a valid integer.")
            continue
        attempts += 1
        if guess < number:
            print("Too low!")
        elif guess > number:
            print("Too high!")
        else:
            print(f"Correct! You guessed the number in {attempts} attempts.")
            break


if __name__ == "__main__":
    main()
