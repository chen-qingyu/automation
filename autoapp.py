# FileName: autoapp.py
# Brief: Python3 script for automating install applications.
# Author: Qing Yu
# CreateDate: 2023.09.27

import os
import platform
import webbrowser
import tomllib
import argparse

from common import COLOR_START, COLOR_INFO, COLOR_FINISH, COLOR_ERROR
from autopip import install_lib


def main():
    # parse command
    parser = argparse.ArgumentParser(prog="autoapp", description="Python3 script for automating install applications.")
    parser.add_argument("name", type=str, help="Python library name or application name", nargs='?', default='')
    args = parser.parse_args()

    # read data
    with open('autoapp.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        apps: list[dict] = data['app']

    if platform.system() != 'Windows':
        print(COLOR_ERROR + "This script currently only supports the Windows platform.\n")
        exit(-1)

    # process command
    install_app(apps if args.name == '' else list(filter(lambda app: app['name'].lower() == args.name.lower(), apps)))


def install_app(apps: list[dict], download_dir: str = f'C:/Users/{os.getlogin()}/Downloads/'):
    try:
        import requests
        import tqdm
    except ModuleNotFoundError:
        install_lib(['requests', 'tqdm'])
        import requests
        import tqdm

    for i, app in zip(range(len(apps)), apps):
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
