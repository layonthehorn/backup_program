#!/usr/bin/env python3

import os
from datetime import datetime
import subprocess
import sys
import re
import gzip


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

    def __str__(self):
        return self.__path

    @property
    def age(self):
        return self.__age

    @property
    def path(self):
        return self.__path


class Backup:
    # backup location
    backup_location = "/mnt/Mass_5400/DriveBackups/"

    # files to back up
    back_ups = ("~/Documents"
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
            age = []
            for file in contents:
                age.append(FileData(os.stat(os.path.join(path, file)).st_mtime,
                                    os.path.join(path, file)))
            age.sort()
            try:
                os.remove(age[0].path)
            except OSError:
                pass

    # this backups the installed packages
    def backup_packages(self):
        self.remove_extra("packages")

        # saves installed packages
        with open(os.path.join(self.backup_location, "packages/installed_packages.txt"), "w") as file:
            subprocess.run(["rpm", "-qa"], stdout=file)

        # saves installed repos
        with open(os.path.join(self.backup_location, "packages/installed_repos.txt"), "w") as file:
            subprocess.run(["dnf", "repolist"], stdout=file)

    def main_backup(self):
        pass


Backup()
