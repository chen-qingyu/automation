# FileName: autoapp.py
# Brief: Python script for automating install applications.
# Author: 青羽 (chen_qingyu@qq.com, https://chen-qingyu.github.io/)
# CreateDate: 2023.09.27
# Copyright (C) 2023

import os
import platform
import webbrowser
import tomllib
import argparse

from common import COLOR_START, COLOR_INFO, COLOR_FINISH, COLOR_ERROR
from autopip import install_pkg


def main():
    # parse command
    parser = argparse.ArgumentParser(prog="autoapp", description="Python3 script for automating install applications.")
    parser.add_argument("command", type=str, help="command", choices=['install'])
    parser.parse_args()

    # read data
    with open('autoapp.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        apps: list[dict] = data['apps']

    if platform.system() != 'Windows':
        print(COLOR_ERROR + "This script currently only supports the Windows platform.\n")
        exit(-1)

    # process command
    install_app(apps)


def install_app(apps: list[dict], download_dir: str = f'C:/Users/{os.getlogin()}/Downloads/'):
    """
    Download and install a list of applications either automatically, manually, or using the `winget` package manager.

    :param apps: a list of dictionaries, where each dictionary represents an app to be installed.
    :type apps: list[dict]
    :param download_dir: specifies the directory where the downloaded files will be saved.
    :type download_dir: str (optional)
    """

    try:
        import requests
        import tqdm
    except ModuleNotFoundError:
        install_pkg(['requests', 'tqdm'])
        import requests
        import tqdm

    for i, app in enumerate(apps):
        print(COLOR_START + f"({i + 1}/{len(apps)}) Start download/install {app['name']}...")

        match app['method']:
            case 'automatic':
                file_name = app['url'].split('/')[-1]
                if not os.path.exists(download_dir + file_name):
                    response = requests.get(app['url'], stream=True)
                    length = int(response.headers.get('content-length', 0))
                    with open(download_dir + file_name, 'wb') as fo, tqdm.tqdm(desc=file_name, total=length, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
                        for data in response.iter_content(chunk_size=1024):
                            size = fo.write(data)
                            bar.update(size)
                os.system(f'{download_dir + file_name} {app['args']}')
                input(COLOR_INFO + "Wait for the installation to complete.")

            case 'manual':
                webbrowser.open(app['site'])
                input(COLOR_INFO + f"Please download and install {app['name']} manually.")

            case 'winget':
                os.system(f'winget install --id {app['id']} --source winget')

            case _:
                print(COLOR_ERROR + "Error: Wrong method.")

        print(COLOR_FINISH + f"Finish download/install {app['name']}.\n")


if __name__ == '__main__':
    main()
