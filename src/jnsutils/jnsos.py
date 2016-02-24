import platform


OS = platform.system()

OS_PREFIX_LINUX = 'linux'
OS_PREFIX_CYGWIN = 'cygwin'
OS_PREFIX_DARWIN = 'darwin'
OS_PREFIX_WINDOWS = 'windows'

def is_linux(os=OS):
    return _is_os(os, OS_PREFIX_LINUX)


def is_cygwin(os=OS):
    return _is_os(os, OS_PREFIX_CYGWIN)


def is_darwin(os=OS):
    return _is_os(os, OS_PREFIX_DARWIN)


def is_windows(os=OS):
    return _is_os(os, OS_PREFIX_WINDOWS)


def _is_os(os, prefix):
    return os and os.lower().startswith(prefix)
