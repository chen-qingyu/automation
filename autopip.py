# FileName: autopip.py
# Brief: Python script for automating install/upgrade packages.
# Author: 青羽 (chen_qingyu@qq.com, https://chen-qingyu.github.io/)
# CreateDate: 2023.12.22
# Copyright (C) 2023

import os
import tomllib
import argparse

from common import COLOR_START, COLOR_INFO, COLOR_FINISH, COLOR_ERROR


def main():
    # parse command
    help_text = """
    install: installs or upgrades a list of packages using pip in Python.
    clean:  cleans up all installed Python packages.
    """
    parser = argparse.ArgumentParser(prog="autopip", description=help_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", type=str, help="command", choices=['install', 'clean'])
    args = parser.parse_args()

    # read data
    with open('autopip.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        pkgs: list[str] = data['packages']

    # process command
    match args.command:
        case 'install':
            install_pkg(pkgs)
        case 'clean':
            clean_pkg()


def install_pkg(pkgs: list[str]):
    """
    Installs or upgrades a list of packages using pip in Python.

    :param pkgs: a list of package names that need to be installed or upgraded
    :type pkgs: list[str]
    """

    print(COLOR_START + f"Start install/upgrade packages: {', '.join(pkgs)}")
    os.system(f'python -m pip install --upgrade {' '.join(pkgs)}')
    os.system('python -m pip cache purge')
    print(COLOR_FINISH + f"Finish install/upgrade packages: {', '.join(pkgs)}")


def clean_pkg():
    """
    Cleans up all installed Python packages.
    """

    print(COLOR_START + f"Start clean packages.")
    os.system('python -m pip freeze > pkgs.txt')
    os.system('python -m pip uninstall --requirement pkgs.txt --yes')
    os.remove('pkgs.txt')
    print(COLOR_FINISH + f"Finish clean packages.")


if __name__ == '__main__':
    main()
