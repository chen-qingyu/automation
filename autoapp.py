# FileName: autoapp.py
# Brief: Python script for automating install applications.
# Author: 青羽 (chen_qingyu@qq.com, https://chen-qingyu.github.io/)
# CreateDate: 2023.09.27
# Copyright (C) 2023

import os
import platform
import subprocess
import webbrowser
import tomllib
import argparse

from common import COLOR_START, COLOR_INFO, COLOR_FINISH, COLOR_ERROR


def main():
    # check platform
    if platform.system() != 'Windows':
        print(COLOR_ERROR + "This script currently only supports the Windows platform.\n")
        exit(-1)

    # parse command
    parser = argparse.ArgumentParser(prog="autoapp", description="Python3 script for automating install applications.")
    parser.add_argument("command", type=str, help="command", choices=['install', 'update', 'check'])
    args = parser.parse_args()

    # read data
    with open('autoapp.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        apps: list[dict] = data['apps']

    # process command
    match args.command:
        case 'install':
            install_app(apps)
        case 'update':
            update_app(apps)
        case 'check':
            check_app(apps)


def install_app(apps: list[dict]):
    """ Install applications using `winget` or manually. """

    for i, app in enumerate(apps, start=1):
        print(COLOR_START + f"({i}/{len(apps)}) Start install {app['name']}...")

        match app['method']:
            case 'winget':
                result = subprocess.run(['winget', 'list', app['id']], capture_output=True, text=True, encoding='utf-8')
                if app['id'] in result.stdout:
                    print(COLOR_INFO + f"{app['name']} is already installed.")
                else:
                    os.system(f'winget install --id {app['id']} --source winget')

            case 'manual':
                webbrowser.open(app['url'])
                input(COLOR_INFO + f"Please install {app['name']} manually.")

            case _:
                print(COLOR_ERROR + "Error: Wrong method.")

        print(COLOR_FINISH + f"Finish install {app['name']}.\n")


def update_app(apps: list[dict]):
    """ Update applications using `winget` or manually. """

    for i, app in enumerate(apps, start=1):
        print(COLOR_START + f"({i}/{len(apps)}) Start update {app['name']}...")

        if app['method'] == 'winget':
            os.system(f'winget upgrade --id {app['id']}')
        else:
            os.system(f'winget search "{app['name']}"')
            input(COLOR_INFO + f"Please update {app['name']} manually.")

        print(COLOR_FINISH + f"Finish update {app['name']}.\n")


def check_app(apps: list[dict]):
    """ Check if applications are installed or available via `winget`. """

    for i, app in enumerate(apps, start=1):
        print(COLOR_START + f"({i}/{len(apps)}) Start check {app['name']}...")

        if app['method'] == 'winget':
            result = subprocess.run(['winget', 'list', app['id']], capture_output=True, text=True, encoding='utf-8')
            if app['id'] in result.stdout:
                print(COLOR_INFO + f"{app['name']} is already installed.")
            else:
                print(COLOR_ERROR + f"{app['name']} is not installed.")
        else:
            os.system(f'winget search "{app['name']}"')
            print(COLOR_INFO + f"Please check {app['name']} manually.")

        print(COLOR_FINISH + f"Finish check {app['name']}.\n")


if __name__ == '__main__':
    main()
