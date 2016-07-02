import os.path


def validate_is_directories(directories):
    for d in directories:
        validate_is_directory(d)


def validate_is_directory(d):
    validate_exists(d, filetype='Directory')
    if not os.path.isdir(d):
        raise NotADirectoryError('Directory is not a directory: {}'.format(d))


def validate_is_files(files):
    for f in files:
        validate_is_file(f)


def validate_is_file(f):
    validate_exists(f)
    if not os.path.isfile(f):
        raise NotADirectoryError('File is not a file: {}'.format(f))


def validate_all_exist(files):
    for f in files:
        validate_exists(f)


def validate_exists(f, filetype='File'):
    if not os.path.exists(f):
        raise FileNotFoundError('{} does not exist: {}'.format(filetype, f))
