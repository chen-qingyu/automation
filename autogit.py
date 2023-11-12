# FileName: autogit.py
# Brief: Python3 script for automating batch manage git repositories.
# Author: Qing Yu
# CreateDate: 2022.02.11

import os
import sys
import tomllib
import argparse

# check version
if not (sys.version_info.major == 3 and sys.version_info.minor >= 12):
    print("Require at least Python >= 3.12")
    exit(1)

# dynamically load third-party libraries
try:
    import colorama
except ModuleNotFoundError:
    os.system('python -m pip install --upgrade --index-url https://pypi.tuna.tsinghua.edu.cn/simple pip setuptools wheel colorama')
    os.system('python -m pip cache purge')
    import colorama

colorama.init(autoreset=True)

COLOR_START = colorama.Fore.BLUE + colorama.Style.BRIGHT
COLOR_INFO = colorama.Fore.CYAN + colorama.Style.BRIGHT
COLOR_FINISH = colorama.Fore.GREEN + colorama.Style.BRIGHT
COLOR_ERROR = colorama.Fore.RED + colorama.Style.BRIGHT

with open('autogit.toml', 'rb') as f:
    DATA = tomllib.load(f)
    SIZE = len(DATA['repos'])
    DATA['repos'].sort(key=lambda repo: os.path.getmtime(repo['local']+repo['name']) if os.path.exists(repo['local']+repo['name']) else 0, reverse=True)


def main():
    help_text = """
    Welcome to the automatic git management program!\n

    status: check repositories status.
    clone:  clone remote repositories to local repositories.
    push:   push local repositories to remote repositories.
    pull:   pull remote repositories to local repositories.
    clean:  clean up redundant files and directories.
    remote: show a list of existing remote repositories.
    gc:     optimize the local repositories.
    """

    parser = argparse.ArgumentParser(prog="autogit", description=help_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", type=str, help="Action of git operation", choices=['status', 'clone', 'push', 'pull', 'clean', 'remote', 'gc'])
    parser.add_argument("name", type=str, help="Abbreviation of repository name", nargs='?', default='')
    args = parser.parse_args()

    options = {'clean': '-d -f -x', 'remote': '--verbose', 'gc': '--aggressive'}
    if args.action == 'clone':
        clone(args.name.lower())
    else:
        process(args.name.lower(), args.action, options.get(args.action, ''))


def exist_path(path) -> bool:
    if not os.path.exists(path):
        print(COLOR_ERROR + f"{path} not exists.")
        return False
    return True


def process(repo_abbr: str, command: str, option: str):
    print(COLOR_START + f"Start {command}.")

    for i, repo in zip(range(SIZE), DATA['repos']):
        if repo_abbr != '' and repo_abbr != repo['abbr'].lower():
            continue

        root = repo['local'] + repo['name']
        print(COLOR_INFO + f"({i + 1}/{SIZE}) {command} {root}:")

        if not exist_path(root):
            continue

        os.chdir(root)
        os.system(f'git {command} {option}')

    print(COLOR_FINISH + f"Finish {command}.")


def clone(name):
    print(COLOR_START + "Start clone.")

    for i, repo in zip(range(SIZE), DATA['repos']):
        if name != '' and name != repo['abbr'].lower():
            continue

        root = repo['local'] + repo['name']
        print(COLOR_INFO + f"({i + 1}/{SIZE}) Cloning {root}:")

        if os.path.exists(root):
            print(COLOR_INFO + f"{root} already exists.")
            continue

        if not os.path.exists(repo['local']):
            os.mkdir(repo['local'])
        os.chdir(repo['local'])
        os.system(f'git clone {repo['remote'][repo['upstream']]} "{repo['name']}"')
        os.chdir(repo['name'])
        for host, url in repo['remote'].items():
            if host != repo['upstream']:
                os.system(f'git remote set-url --add origin {url}')

    print(COLOR_FINISH + "Finish clone.")


if __name__ == '__main__':
    main()
