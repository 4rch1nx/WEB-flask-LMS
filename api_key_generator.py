import string
import random

all_letters_list = [string.ascii_letters,
                    string.digits]


def generate_api_key():
    api_key = ""
    for i in range(random.randint(20, 30)):
        letter = get_random_letter()
        while api_key.count(letter) > 5:
            letter = get_random_letter()
        api_key += letter
    return api_key


def get_random_letter():
    letters_list = all_letters_list[random.randint(0, 1)]
    letter = letters_list[random.randint(0, len(letters_list) - 1)]
    return letter

