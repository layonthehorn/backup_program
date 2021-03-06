#!/usr/bin/env python3

import os
import json
import sys
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


def open_json():
    backup_locations = []
    json_file = open("backuplist.json")
    json_dict = json.load(json_file)
    json_file.close()
    for key in json_dict:
        backup_locations.append(json_dict[key])

    return tuple(backup_locations)


class Backup:
    def __init__(self, backup_location: str, save_packages: bool = False):
        self.backup_location = backup_location

        # if backup file exists get info from it
        if os.path.exists("backuplist.json"):
            locations = open_json()
        # otherwise run defaults
        else:
            locations = (
                ".config",
                "Music",
                "Videos",
                "Pictures",
                "Documents",
                "Games",
            )
        if os.path.exists(self.backup_location):
            if save_packages:
                self.backup_packages()
            for location in locations:
                p: Process = Process(target=self.backup_folder, args=(location,))
                p.start()
        else:
            print(f"Error, Backup Directory {self.backup_location} does not exist.")

    def remove_extra(self, dir_name: str) -> None:
        path = os.path.join(self.backup_location, dir_name)

        # if the back up folder does not exist it
        # creates it.
        if not os.path.exists(path):
            os.mkdir(path)
        contents = os.listdir(path)
        if len(contents) >= 3:
            # a list of all the files found
            age: List[FileData] = []
            for file in contents:
                age.append(
                    FileData(
                        os.stat(os.path.join(path, file)).st_mtime,
                        os.path.join(path, file),
                    )
                )
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
        compressed_name: str = os.path.join(
            self.backup_location, f"packages/package_{datetime.now()}"
        )

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
        compressed_name: str = os.path.join(
            self.backup_location,
            f"{new_folder}/{new_folder}_{datetime.now()}",
        )
        if os.path.exists(f"/home/{getpass.getuser()}/{folder}"):
            shutil.make_archive(
                compressed_name, "gztar", f"/home/{getpass.getuser()}/{folder}"
            )
        else:
            with open(os.path.join(self.backup_location, f"{new_folder}/Error_{datetime.now()}"), "w") as file:
                file.write(f"Could not find /home/{getpass.getuser()}/{folder}")


if __name__ == "__main__":

    # if you give two arguments
    if len(sys.argv) > 2:
        folder = sys.argv[1]
        packages = sys.argv[2]
        if packages.lower() == "true":
            Backup(folder, True)
        elif packages.lower() == "false":
            Backup(folder)
        else:
            print(f"Unknown Value {packages}, expected (True/False)")

    # if you give a single argument defaults to not saving packages
    elif len(sys.argv) > 1:
        folder = sys.argv[1]
        Backup(folder)

    # if you give no arguments
    else:
        print("Needs an argument for the backup storage location.")
        print(
            "Optionally, true/false for package backup - Warning: Only works on Fedora Linux."
        )
        print(f"{sys.argv[0]} (Backup Storage) (True/False)")
        sys.exit(0)
