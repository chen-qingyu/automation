# FileName: autopip.py
# Brief: Python script for automating install/upgrade packages.
# Author: 青羽 (chen_qingyu@qq.com, https://chen-qingyu.github.io/)
# CreateDate: 2023.12.22
# Copyright (C) 2023-2025

import os
import tomllib
import argparse

from common import COLOR_START, COLOR_FINISH


def main():
    help_text = """
    install: install or upgrade a list of packages using pip in Python.
    clean:   clean up all installed Python packages.
    """

    # parse command
    parser = argparse.ArgumentParser(prog="autopip", description=help_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", type=str, choices=['install', 'clean'])
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
    """ Install or upgrade a list of packages using pip in Python. """

    print(COLOR_START + f"Start install/upgrade packages: {', '.join(pkgs)}")
    os.system('py -m pip install --upgrade -i https://mirrors.aliyun.com/pypi/simple/ pip')
    os.system(f'py -m pip install --upgrade -i https://mirrors.aliyun.com/pypi/simple/ {' '.join(pkgs)}')
    os.system('py -m pip cache purge')
    print(COLOR_FINISH + f"Finish install/upgrade packages: {', '.join(pkgs)}")


def clean_pkg():
    """ Clean up all installed Python packages. """

    print(COLOR_START + "Start clean packages.")
    os.system('py -m pip freeze > pkgs.txt')
    os.system('py -m pip uninstall --requirement pkgs.txt --yes')
    os.remove('pkgs.txt')
    print(COLOR_FINISH + "Finish clean packages.")


if __name__ == '__main__':
    main()
