import json
import os
import re
import subprocess

from kalplib import kutils


PACK_JSON_FNAME = 'package.json'
PACK_JSON_DEV_DEPS_KEY = 'devDependencies'
PACK_JSON_DEPS_KEY = 'dependencies'
PACK_JSON_VERSION_KEY = 'version'
NODE_MODULES_DIR = 'node_modules'


def get_package_json(root):
    package_json_dir = kutils.find_file_up_hierarchy(root, PACK_JSON_FNAME)
    package_json = None
    
    if package_json_dir is None:
        raise FileNotFoundError(kutils.format_error(
            'Could not check if npm install needed becuase "{}" could not be found.'.format(PACK_JSON_FNAME)))
    
    with open(os.path.join(package_json_dir, PACK_JSON_FNAME)) as package_json_data:
        package_json = json.load(package_json_data)
    
    return package_json_dir, package_json


def get_uninstalled_dependencies(package_json_dir, package_json):
    dev_deps = set(get_uninstalled_dependencies_of_type(PACK_JSON_DEV_DEPS_KEY, package_json_dir, package_json))
    deps = set(get_uninstalled_dependencies_of_type(PACK_JSON_DEPS_KEY, package_json_dir, package_json))
    
    return dev_deps.union(deps)


def get_uninstalled_dependencies_of_type(dependency_type, package_json_dir, package_json):
    it = iter(package_json.get(dependency_type, []))
    return [dep for dep in it if not is_dependency_installed(package_json_dir, dep)]


def is_dependency_installed(package_json_dir, dependency):
    return os.path.isdir(os.path.join(package_json_dir, NODE_MODULES_DIR, str(dependency)))


def get_out_of_date_dependencies(package_json_dir, package_json):
    dev_deps = set(get_out_of_date_dependencies_of_type(PACK_JSON_DEV_DEPS_KEY, package_json_dir, package_json))
    deps = set(get_out_of_date_dependencies_of_type(PACK_JSON_DEPS_KEY, package_json_dir, package_json))
    
    return dev_deps.union(deps)


def get_out_of_date_dependencies_of_type(dependency_type, package_json_dir, package_json):
    it = iter(package_json.get(dependency_type, []))
    return [dep for dep in it if not is_dependency_is_up_to_date(dependency_type, package_json_dir, package_json, dep)]


def is_dependency_is_up_to_date(dependency_type, package_json_dir, package_json, dependency):
    expected_version = package_json[dependency_type][dependency]
    actual_version = None
    up_to_date = False
    
    try:
        with open(os.path.join(package_json_dir, NODE_MODULES_DIR, dependency, PACK_JSON_FNAME)) as package_json_data:
            actual_version = json.load(package_json_data)[PACK_JSON_VERSION_KEY]
        
        up_to_date = is_version_is_up_to_date(expected_version, actual_version)
    except FileNotFoundError:  # Some packages don't actually have a package.json
        up_to_date = True

    return up_to_date


def is_version_is_up_to_date(expected_version, actual_version):
    up_to_date = False
    
    if expected_version.startswith('^') or expected_version.startswith('~'):
        e_major, e_minor, e_patch = parse_version(expected_version)
        a_major, a_minor, a_patch = parse_version(actual_version)
        
        # major version
        if e_major < a_major:
            up_to_date = True
        elif e_major > a_major:
            up_to_date = False
        # minor version
        elif e_minor < a_minor:
            up_to_date = True
        elif e_minor > a_minor:
            up_to_date = False
        # patch
        else:
            up_to_date = e_patch <= a_patch
    else:
        up_to_date = expected_version == actual_version
    
    return up_to_date


def parse_version(version):
    parts = version.split(sep='.')
    major = int(re.findall(r'\d+', parts[0])[0])
    minor = int(re.findall(r'\d+', parts[1])[0])
    patch = int(re.findall(r'\d+', parts[2])[0])
    
    return major, minor, patch


def npm_install(package_json_dir):
    popen = subprocess.Popen(['npm', 'install'], cwd=package_json_dir)
    popen.wait()
