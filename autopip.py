# FileName: autopip.py
# Brief: Python3 script for automating install/upgrade packages.
# Author: Qing Yu
# CreateDate: 2023.12.22

import os
import tomllib
import argparse

from common import COLOR_START, COLOR_INFO, COLOR_FINISH, COLOR_ERROR


def main():
    # parse command
    parser = argparse.ArgumentParser(prog="autopip", description="Python3 script for automating install/upgrade packages.")
    args = parser.parse_args()

    # read data
    with open('autopip.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        libs: list[str] = data['packages']

    # process command
    install_lib(libs)


def install_lib(libs: list[str]):
    print(COLOR_START + f"Start install/upgrade libraries: {', '.join(libs)}")
    os.system(f'python -m pip install --upgrade {' '.join(libs)}')
    os.system('python -m pip cache purge')
    print(COLOR_FINISH + f"Finish install/upgrade libraries: {', '.join(libs)}")


if __name__ == '__main__':
    main()
