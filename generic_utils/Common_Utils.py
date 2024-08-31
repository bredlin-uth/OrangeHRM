import datetime
import os
import random
import re

from generic_utils import Config_Utils


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


def get_recent_file(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    # Filter for files that end with common download file extensions
    download_extensions = ['.zip', '.rar', '.exe', '.pdf', '.docx', '.xlsx', '.jpg', '.png', '.mp4', '.mp3', '.txt']
    download_files = [file for file in files if file.endswith(tuple(download_extensions))]
    if download_files:
        # Get the creation time for each download file
        file_creation_times = [(os.path.getmtime(os.path.join(directory, file)), file) for file in download_files]
        # Sort the files by creation time in descending order
        file_creation_times.sort(reverse=True)
        # Return the name of the most recently downloaded file
        return file_creation_times[0][1]
    else:
        return None
