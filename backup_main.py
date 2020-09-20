#!/usr/bin/env python3

import os
from typing import List, Tuple
from datetime import datetime
import subprocess
import shutil
import sys
import re


class FileData:
    """A clean class to hold a small about of file data together."""

    def __init__(self, age: float, path: str):
        self.__age = age
        self.__path = path

    def __lt__(self, other):
        return self.age < other.age

    def __gt__(self, other):
        return self.age > other.age

    def __eq__(self, other):
        return self.age == other.age and self.path == other.path

    @property
    def age(self):
        return self.__age

    @property
    def path(self):
        return self.__path


class Backup:
    # backup location
    backup_location: str = "/mnt/Mass_5400/DriveBackups/"

    # files to back up
    back_ups: Tuple[str] = ("~/Documents"
                            , "~/Music"
                            , "~/Videos"
                            , "~/Pictures"
                            , "~/.config"
                            , "~/Games")

    def __init__(self):
        self.backup_packages()
        self.main_backup()

    def remove_extra(self, dir_name: str) -> None:
        path = os.path.join(self.backup_location, dir_name)
        contents = os.listdir(path)
        if len(contents) >= 3:
            # a list of all the files found
            age: List[FileData] = []
            for file in contents:
                age.append(FileData(os.stat(os.path.join(path, file)).st_mtime,
                                    os.path.join(path, file)))
            age.sort()
            try:
                os.remove(age[0].path)
            except OSError:
                pass

    # this backups the installed packages
    def backup_packages(self) -> None:
        self.remove_extra("packages")
        if not os.path.exists("/tmp/temp_folder"):
            os.mkdir("/tmp/temp_folder")
        repos: str = "/tmp/temp_folder/installed_repos.txt"
        packages: str = "/tmp/temp_folder/installed_packages.txt"
        base_name: str = os.path.join(self.backup_location, "packages")
        compressed_name: str = os.path.join(self.backup_location, f"packages/package_{datetime.now()}")

        # saves installed packages
        with open(packages, "w") as file:
            subprocess.run(["rpm", "-qa"], stdout=file)

        # saves installed repos
        with open(repos, "w") as file:
            subprocess.run(["dnf", "repolist"], stdout=file)

        shutil.make_archive(compressed_name, "gztar", "/tmp/temp_folder")

    def main_backup(self) -> None:
        pass


Backup()
