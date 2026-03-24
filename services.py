import random

library = []


def validate_string(prompt: str) -> str:
    """
    this function makes sure that an empty space is not returned
    and the text returned must be greater or equal to three characters
    :param prompt: user input
    :return: str value
    """
    while True:
        text = input(prompt).strip()
        if text and len(text) >= 3:
            return text
        print("Input cannot be empty")


def validate_numbers(prompt: str) -> int:
    """
    this function makes sure that negative numbers or decimal numbers are not returned
    :param prompt: it takes a string input
    :return: a string
    """
    while True:
        num = input(prompt)
        if num.isnumeric() and len(num) == 4:
            return int(num)
        print("Invalid year")


def rating():
    """
    this function generates random numbers between, 1 to 10
    if the number is between, 1 to 5, it returns the number
    otherwise it returns None
    :return: int or None
    """
    num = random.randint(1, 10)
    if num <= 5:
        return num

    return None

