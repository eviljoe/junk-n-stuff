import platform


OS = platform.system()

OS_PREFIX_LINUX = 'linux'
OS_PREFIX_CYGWIN = 'cygwin'
OS_PREFIX_DARWIN = 'darwin'
OS_PREFIX_WINDOWS = 'windows'


def is_linux(os=OS):
    return is_os(OS_PREFIX_LINUX, os=os)


def is_cygwin(os=OS):
    return is_os(OS_PREFIX_CYGWIN, os=os)


def is_darwin(os=OS):
    return is_os(OS_PREFIX_DARWIN, os=os)


def is_windows(os=OS):
    return is_os(OS_PREFIX_WINDOWS, os=os)


def is_os(prefix, os=OS):
    return os and os.lower().startswith(prefix)
