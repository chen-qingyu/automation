# FileName: autogit.py
# Brief: Python script for automating batch manage git repositories.
# Author: 青羽 (chen_qingyu@qq.com, https://chen-qingyu.github.io/)
# CreateDate: 2022.02.11
# Copyright (C) 2022 - 2023

import os
import tomllib
import argparse

from common import COLOR_START, COLOR_INFO, COLOR_FINISH, COLOR_ERROR


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
    parser.add_argument("command", type=str, help="Git command", choices=['status', 'clone', 'push', 'pull', 'clean', 'remote', 'gc'])
    args = parser.parse_args()

    # read data
    with open('autogit.toml', 'rb') as f:
        data: dict = tomllib.load(f)
        repos: list[dict] = data['repos']
        repos.sort(key=lambda repo: os.path.getmtime(repo['path']) if os.path.exists(repo['path']) else 0, reverse=True)

    process_command(repos, args.command)


def process_command(repos: list[dict], command: str):
    """
    Takes a list of repositories and a command as input, and performs the specified command on each repository.

    :param repos: a list of dictionaries. Each dictionary represents a repository.
    :type repos: list[dict]
    :param command: a string that represents the git action to be performed.
    :type command: str
    """

    print(COLOR_START + f"Start {command}.")

    for i, repo in enumerate(repos):
        print(COLOR_INFO + f"({i + 1}/{len(repos)}) {command} {repo['path']}:")

        if command == 'clone':
            if os.path.exists(repo['path']):
                print(COLOR_INFO + f"{repo['path']} already exists.")
                continue

            os.system(f'git clone {repo['remote'][repo['upstream']]} "{repo['path']}"')
            os.chdir(repo['path'])
            for host, url in repo['remote'].items():
                if host != repo['upstream']:
                    os.system(f'git remote set-url --add origin {url}')

        else:
            if not os.path.exists(repo['path']):
                print(COLOR_ERROR + f"{repo['path']} not exists.")
                continue

            os.chdir(repo['path'])
            option = {'clean': '-d -f -x', 'remote': '--verbose', 'gc': '--aggressive'}.get(command, '')
            os.system(f'git {command} {option}')

    print(COLOR_FINISH + f"Finish {command}.")


if __name__ == '__main__':
    main()
