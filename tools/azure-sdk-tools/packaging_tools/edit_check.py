import argparse
import logging
import os
from pathlib import Path
import re
import time

_LOGGER = logging.getLogger(__name__)

_VER_OLD = '0.0.0'
_VER_NEW = '0.0.0'


def calcu_version(md_output):
    global _VER_NEW
    flag = [False, False, True]  # breaking,feature,bugfix
    if md_output.find('**Breaking changes**') > -1:
        flag[0] = True
    elif md_output.find('**Features**') > -1:
        flag[1] = True

    num = _VER_OLD.split('.')
    result = re.search('[a-z]+', _VER_OLD)
    if result:
        alpha = result.group()
        lastnum = num[2].split(alpha)
        lastnum[1] = str(int(lastnum[1]) + 1)
        _VER_NEW = f'{num[0]}.{num[1]}.{lastnum[0]}{alpha}{lastnum[1]}'
    elif flag[0]:
        _VER_NEW = f'{int(num[0]) + 1}.0.0'
    elif flag[1]:
        _VER_NEW = f'{num[0]}.{int(num[1]) + 1}.0'
    elif flag[2]:
        _VER_NEW = f'{num[0]}.{num[1]}.{int(num[2]) + 1}'


def edit_changelog(basic_folder, md_output):
    changlog_file = str(Path(basic_folder, 'CHANGELOG.md'))
    with open(changlog_file, 'r') as file:
        content = file.readlines()
        out_content = [content[0] + '\n']
        date = time.localtime(time.time())
        out_content.append('## {} ({}-{:02d}-{:02d})\n\n'.format(_VER_NEW, date.tm_year, date.tm_mon, date.tm_mday))
        list_changelog = md_output.split('\\n')
        list_output = [line + '\n' for line in list_changelog]
        out_content.extend(list_output)
        list_output.append('\n')
        out_content.extend(content[1:])
    with open(changlog_file, 'w') as file:
        file.writelines(out_content)


def replace_bad_name(basic_folder, service_name):
    for file in os.listdir(basic_folder):
        file_name = str(Path(basic_folder, file))
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file_in:
                content = file_in.readlines()
            out = [re.sub('myservice', service_name.capitalize(), line, flags=re.IGNORECASE) for line in content]
            with open(file_name, 'w') as file_out:
                file_out.writelines(out)


def check_release_history(package_name):
    from pypi_tools.pypi import PyPIClient
    client = PyPIClient()
    versions = [str(v) for v in client.get_ordered_versions(package_name)]
    if _VER_OLD not in versions:
        _LOGGER.warning(f'Please notice {_VER_OLD} has not been released, you can use it again')


def edit_version(version_file, md_output):
    global _VER_OLD
    with open(version_file, 'r') as file_in:
        version_content = file_in.readlines()
        for i in range(0, len(version_content)):
            if version_content[i].find('VERSION') > -1:
                result = re.search('\".+\"', version_content[i])
                _VER_OLD = result.group().replace('\"', '')
                calcu_version(md_output)
                version_content[i] = version_content[i].replace(_VER_OLD, _VER_NEW)
                break
    with open(version_file, 'w') as file_out:
        file_out.writelines(version_content)


def main(sdk_folder, folder_name, package_name, md_output):
    service_name = package_name.replace('azure-mgmt-', '')
    basic_folder = str(Path(sdk_folder, folder_name, package_name))
    version_folder = str(Path(basic_folder, 'azure', 'mgmt', service_name))
    version_file = str(Path(version_folder, 'version.py'))
    if not os.path.exists(version_file):
        version_file = str(Path(version_folder, '_version.py'))
    if not os.path.exists(version_file):
        return
    # edit version.py
    edit_version(version_file, md_output)
    # edit changelog
    edit_changelog(basic_folder, md_output)
    # do some check
    replace_bad_name(basic_folder, service_name)
    check_release_history(package_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sdk_folder', help='Work folder.')
    parser.add_argument('folder_name', help='specific folder.')
    parser.add_argument('package_name', help='release package name.')
    parser.add_argument('md_output', help='addtional changelog.')
    args = parser.parse_args()
    main(args.sdk_folder, args.folder_name, args.package_name, args.md_output)
