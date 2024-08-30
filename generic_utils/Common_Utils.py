import datetime
import os
import random
import re


def generate_random_number(digits):
    digits = [str(random.randint(0, 9)) for _ in range(digits)]
    random_number = int(''.join(digits))
    return random_number


def split_sentence(sentence, delimiter=None):
    if delimiter is None:
        # If no delimiter is specified, default to splitting by spaces
        words = sentence.split()
    else:
        words = sentence.split(delimiter)
    return words

def get_timestamp():
    #  "%Y/%m/%d %H:%M:%S %a %p"
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def split_string(input_string):
    # Use regular expression to split the string at the apostrophe
    parts = re.split(r"[\\]", input_string)
    # Strip leading and trailing spaces from each part
    parts = [part.strip() for part in parts]
    return parts

def create_folder_with_timestamp(folder_path, timestamp):
    folder_name = f"{folder_path}_{timestamp}"
    try:
        os.mkdir(folder_name)
        return folder_name
    except FileExistsError:
        print(f"Folder already exists: {folder_name}")

