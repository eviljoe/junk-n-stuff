#!/usr/bin/env python3


import argparse
import os.path
import sys

from jnscommons import jnsstr
from jnscommons import jnsvalid


PRIORITY_SEPARATOR = '@'
DEFAULT_PRIORITY = '0'

ERR_NONE = 0
ERR_NO_VPN_SPECS = 1
ERR_VPN_CONFIG_FILE_DNE = 2
ERR_COULD_NOT_CONNECT = 3


########
# Main #
########


def main():
    exit_code = ERR_NONE
    
    opts = _parse_args()
    vpn_specs = _get_vpn_specs(opts)
    
    if vpn_specs:
        _parse_vpn_specs(vpn_specs)
    else:
        exit_code = ERR_NO_VPN_SPECS
        print('No VPN configuration specified', file=sys.stderr)
    
    if exit_code == 0:
        exit_code = _validate_vpn_specs(vpn_specs)
    
    if exit_code == 0:
        if not _try_connections(vpn_specs):
            exit_code = ERR_COULD_NOT_CONNECT
            print('Could not connect', file=sys.stderr)
    
    sys.exit(exit_code)


################################
# Command Line Args. Functions #
################################


def _parse_args():
    parser = argparse.ArgumentParser(description='Connect to a VPN', epilog=_create_help_epilog(),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Just output what actions will be peformed without actually performing them')
    parser.add_argument('vpn_configs', nargs='*', metavar='vpn_config', default=[],
                        help='The VPN configuration specifications.  Should be in the format described below')
    
    return parser.parse_args()


def _create_help_epilog():
    basename = os.path.basename(sys.argv[0])
    e = []
    
    e.append('VPN CONFIGURATION FORMAT')
    e.append('Each VPN file declaration should be in the following format:')
    e.append('    [PRIORITY{}]<OPENVPN_FILE_PATH>'.format(PRIORITY_SEPARATOR))
    e.append('The PRIORITY can be any string.  It will be used to sort the openvpn configurations files in the order '
             'that they will be used.  If PRIORITY is ommitted, "0" will be used as that file\'s PRIORITY.  The '
             'OPENVPN_FILE_PATH is used to locate the openvpn configuration files that will be used to connect to the '
             'VPN.')
    e.append('')
    e.append('CONFIGURATION FILE')
    e.append('In addition to the command line arguments, a configuration file can be used to specify the openvpn '
             'configuration files that should be used.  `{}\' will look for that file here for the configuration '
             'file:'.format(basename))
    e.append('    {}'.format(_get_default_config_file_name()))
    e.append('Each line of the file should be in the format described above.')
    e.append('')
    e.append('CONFIGURATION FILE NOTES')
    e.append(' * Empty lines and lines containing only whitespace are ignored.')
    e.append(' * Lines whose priority starts with # are ignored.')
    e.append(' * The priority and file path can contain whitespace, but whitespace will be trimmed from the start and '
             'end of both the priority and file path.')
    e.append(' * If configurations are specified on the command line, the configurations in the file will be ignored.')
    
    return jnsstr.wrap_str_array(e)


######################
# VPN Spec Functions #
######################


def _get_vpn_specs(opts):
    vpn_specs = _get_vpn_specs_from_opts(opts)
    
    if not vpn_specs:
        vpn_specs = _get_vpn_specs_from_file()
    
    return vpn_specs


def _get_vpn_specs_from_opts(opts):
    vpn_specs = []
    
    for vpn_config in opts.vpn_configs:
        vpn_config = vpn_config.strip() if vpn_config else vpn_config
        
        if vpn_config:
            vpn_specs.append(VPNFileSpec(raw=vpn_config))
        
    return vpn_specs


def _get_vpn_specs_from_file():
    config_file_name = _get_default_config_file_name()
    vpn_specs = []
    
    if os.path.isfile(config_file_name):
        with open(config_file_name, 'r') as config_file:
            line = 0
            
            for line in config_file:
                line += 1
                line = line.strip() if line else line
                
                if line and not line.startswith('#'):
                    vpn_specs.append(VPNFileSpec(raw=line, line=line))
    
    return vpn_specs


def _parse_vpn_specs(vpn_specs):
    for vpn_spec in vpn_specs:
        _parse_vpn_spec(vpn_spec)


def _parse_vpn_spec(vpn_spec):
    priority_sep_index = vpn_spec.raw.find(PRIORITY_SEPARATOR)
    
    if priority_sep_index == -1:
        vpn_spec.priority = DEFAULT_PRIORITY
        vpn_spec.file_path = vpn_spec.raw
    elif priority_sep_index == 0:
        vpn_spec.priority = DEFAULT_PRIORITY
        vpn_spec.file_path = vpn_spec.raw[1:]
    else:
        vpn_spec.priority = vpn_spec.raw[:priority_sep_index]
        vpn_spec.file_path = vpn_spec.raw[priority_sep_index + 1:]


def _validate_vpn_specs(vpn_specs):
    vpn_spec_count = len(vpn_specs)
    err = ERR_NONE
    index = 0
    
    while index < vpn_spec_count and err == 0:
        err = _validate_vpn_spec(vpn_specs[index])
        index += 1
    
    return err


def _validate_vpn_spec(vpn_spec):
    err = ERR_NONE
    
    try:
        jnsvalid.validate_is_file(vpn_spec.file_path)
    except FileNotFoundError:
        err = ERR_VPN_CONFIG_FILE_DNE
        line = 'Line {}: '.format(vpn_spec.line) if vpn_spec.line is not None else ''
        print('{}File does not exist or is not a file: "{}"'.format(line, vpn_spec.file_path), file=sys.stderr)
    
    return err


############################
# VPN Connection Functions #
############################


def _try_connections(vpn_specs):
    connected = False
    
    for vpn_spec in sorted(vpn_specs, key=lambda vs: vs.priority):
        print(vpn_spec.file_path)  # TODO try to connect instead of just printing this
    
    return connected


###################
# Misc. Functions #
###################


def _get_default_config_file_name():
    return os.path.join(os.path.expanduser('~'), '.jns', 'tread')


###########
# Classes #
###########


class VPNFileSpec:
    def __init__(self, raw=None, line=None, priority=None, file_path=None):
        self.raw = raw
        self.line = line
        self.priority = priority
        self.file_path = file_path


##############
# Main Check #
##############

if __name__ == '__main__':
    main()
