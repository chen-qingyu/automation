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
        print(COLOR_ERROR + "This script only supports Windows.\n")
        exit(-1)

    help_text = """
    install: install applications using `winget` or manually.
    update:  update applications using `winget` or manually.
    check:   check if applications are installed or available via `winget`.
    """

    # parse command
    parser = argparse.ArgumentParser(prog="autoapp", description=help_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", type=str, help="command", choices=['install', 'update', 'check'])
    args = parser.parse_args()

    # read data
    with open('autoapp.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        apps: list[dict] = data['apps']

    # process command
    process_command(args.command, apps)


def process_command(command: str, apps: list[dict]):
    for i, app in enumerate(apps, start=1):
        print(COLOR_START + f"({i}/{len(apps)}) Start install {app['name']}...")

        match (command, app['method']):
            case ('install' | 'check', 'winget'):
                result = subprocess.run(['winget', 'list', app['id']], capture_output=True, text=True, encoding='utf-8')
                if app['id'] in result.stdout:
                    print(COLOR_INFO + f"{app['name']} is already installed.")
                elif command == 'install':
                    os.system(f'winget install --id {app['id']} --source winget')
                elif command == 'check':
                    print(COLOR_ERROR + f"{app['name']} is not installed.")

            case ('update', 'winget'):
                os.system(f'winget upgrade --id {app['id']}')

            case ('install' | 'update', 'manual'):
                webbrowser.open(app['url'])
                input(COLOR_INFO + f"Please {command} {app['name']} manually.")

            case ('check', 'manual'):
                os.system(f'winget search "{app['name']}"')
                print(COLOR_INFO + f"Please check {app['name']} manually.")

            case _:
                print(COLOR_ERROR + "Error: Wrong method.")

        print(COLOR_FINISH + f"Finish {command} {app['name']}.\n")


if __name__ == '__main__':
    main()
