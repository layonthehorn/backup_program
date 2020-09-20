#!/usr/bin/env python3

import os
import getpass
from typing import List
from datetime import datetime
import subprocess
import shutil
from multiprocessing import Process


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

    def __init__(self):
        if os.path.exists(self.backup_location):
            self.backup_packages()
            for location in (".config", "music", "videos", "pictures", "documents", "games"):
                p = Process(target=self.backup_folder, args=(location,))
                p.start()
        else:
            print(f"Error, Backup Directory {self.backup_location} does not exist.")

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
        compressed_name: str = os.path.join(self.backup_location, f"packages/package_{datetime.now()}")

        # saves installed packages
        with open(packages, "w") as file:
            subprocess.run(["rpm", "-qa"], stdout=file)

        # saves installed repos
        with open(repos, "w") as file:
            subprocess.run(["dnf", "repolist"], stdout=file)

        shutil.make_archive(compressed_name, "gztar", "/tmp/temp_folder")

    def backup_folder(self, folder: str) -> None:
        # only for .config archive to not be hidden
        if folder.startswith("."):
            new_folder: str = folder[1:]
        else:
            new_folder: str = folder
        self.remove_extra(new_folder)
        compressed_name: str = os.path.join(self.backup_location, f"{new_folder}/{new_folder.capitalize()}_{datetime.now()}")

        shutil.make_archive(compressed_name, "gztar", f"/home/{getpass.getuser()}/{folder.capitalize()}")


Backup()
