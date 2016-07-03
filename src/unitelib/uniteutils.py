from unitelib.archivers import jar
from unitelib.archivers import tar
from unitelib.archivers import targz
from unitelib.archivers import tarbz2
from unitelib.archivers import zzip


# ######### #
# Constants #
# ######### #


# The order of the archiver in this array matters.  This will be the order that each archiver is checked when
# determining the archiver for a particular file.  For example, the "tar.gz" archiver needs to be before the "gz"
# archiver so the "gz" archiver is not always used instead of the "tar.gz" archiver.
ARCHIVERS = [
    tar.TARArchiver(),
    targz.TARGZArchiver(),
    tarbz2.TARBZ2Archiver(),
    jar.JARArchiver(),
    zzip.ZipArchiver()
]


# ################# #
# Utility Functions #
# ################# #


def get_archiver(fmt, file_name):
    return get_archiver_for_format(fmt) if fmt else get_archiver_for_file_name(file_name)


def get_archiver_for_format(fmt):
    archiver = next((a for a in ARCHIVERS if _is_in_file_extensions(fmt, a.get_file_extensions())), None)
    
    if not archiver:
        raise UnsupportedArchiveFormatError('Cannot determine archive type from format: {}'.format(fmt))
    
    return archiver


def _is_in_file_extensions(ext, exts):
    l_ext = ext.lower()
    return next((e for e in exts if l_ext == e.lower()), None) is not None


def get_archiver_for_file_name(fname):
    archiver = next((a for a in ARCHIVERS if _does_archiver_have_ext_for_file(a, fname)), None)
    
    if not archiver:
        raise UnsupportedArchiveFormatError('Cannot determine archive type from file name: {}'.format(fname))
    
    return archiver


def _does_archiver_have_ext_for_file(archiver, fname):
    l_fname = fname.lower()
    return next((e for e in archiver.get_file_extensions() if l_fname.endswith('.' + e.lower())), None) is not None


# ########## #
# Exceptions #
# ########## #


class UnsupportedArchiveFormatError(Exception):
    pass
