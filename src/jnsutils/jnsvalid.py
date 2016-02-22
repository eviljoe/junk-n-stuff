import os.path


def validate_is_directories(directories):
    for directory in directories:
        validate_is_directory(directory)


def validate_is_directory(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError('Directory does not exist: {}'.format(directory))
    elif not os.path.isdir(directory):
        raise NotADirectoryError('Directory is not a directory: {}'.format(directory))
