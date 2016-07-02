from unitelib.archivers import zzip
from unitelib.archivers import targz


# ######### #
# Constants #
# ######### #


# The order of the archiver in this array matters.  This will be the order that each archiver is checked when
# determining the archiver for a particular file.  For example, the "tar.gz" archiver needs to be before the "gz"
# archiver so the "gz" archiver is not always used instead of the "tar.gz" archiver.
ARCHIVERS = [
    targz.TARGZArchiver(),
    # JOE todo tar.bz2
    # JOE todo tar
    # JOE todo gz
    # JOE todo bz2
    zzip.ZipArchiver()
]


# ################# #
# Utility Functions #
# ################# #


def get_archiver(fmt, file_name):
    return get_archiver_for_format(fmt) if fmt else get_archiver_for_file_name(file_name)


def get_archiver_for_format(fmt):
    archiver = next((a for a in ARCHIVERS if fmt == a.file_extension()), None)
    
    if not archiver:
        raise UnsupportedArchiveFormatError('Cannot determine archive type from format: {}'.format(fmt))
    
    return archiver


def get_archiver_for_file_name(file_name):
    archiver = next((a for a in ARCHIVERS if file_name.endswith(a.file_extension())), None)
    
    if not archiver:
        raise UnsupportedArchiveFormatError('Cannot determine archive type from file name: {}'.format(file_name))
    
    return archiver


# ########## #
# Exceptions #
# ########## #


class UnsupportedArchiveFormatError(Exception):
    pass
