# Backup Program
This is a simple backup program written in Python. 
It uses Python multiprocessing to back up several folders at once.

## Default Folders
* **.config**
* **Documents**
* **Music**
* **Videos**
* **Pictures**
* **Games**

It also saves the installed packages and repos if you are using Fedora Linux.

## Usage
To use this you would either schedule its run it with a cronjob or do it yourself manually.
You need to provide an argument for the backup storage location, and it will
create the required folders within it.\
Optionally you can tell it to back up your installed packages and repos. Note: This only works on Fedora Linux.

### JSON Support
It can also use json files to customize the folders it backs up. Fill it out in the format that follows.\
It uses relative paths from your home directory. If there is no JSON file it uses the defaults as above.

{"1" : ".config",\
"2" : "Music",\
"3" : "Videos",\
"4" : "Pictures",\
"5" : "Documents",\
"6" : "Games"}

Simply create the file "backuplist.json" next to the main file. The program does nothing with the "keys" it only uses the paths next to them.
### Manual Running
* **backup_main.py** (**storage_folder**) (**True**/**False**)

### Cron Running
* \* \* \* \* \* **/path/to/script/backup_main.py /path/to/storage true** 
