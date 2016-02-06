import os


BOLD = '\033[1m'
CYAN = '\033[36m'
MAGENTA = '\033[35m'
RED = '\033[31m'
PLAIN = '\033[0m'


# ################# #
# Utility Functions #
# ################# #


def find_file_up_hierarchy(root, file):
    next_path = root
    path = None
    found = False
    
    while not found and path != next_path:
        path = next_path
        found = file in os.listdir(path)
        next_path = os.path.dirname(path)
    
    return path if found else None


def format_error(text):
    return format_string(text, BOLD, RED)


def format_string(text, *formats):
    return ''.join(formats) + text + PLAIN


def print_formatted(text, *formats):
    print(format_string(text, *formats))


def print_titled(title, title_format, text, text_format):
    print(format_string(title, *title_format), end='')
    print(format_string(text, *text_format))
