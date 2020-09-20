# Backup Program
This is a simple backup program written in python. 
It uses multiprocessing to backup several folders at once.
* .config
* Documents
* Music
* Videos
* Pictures
* Games

It also saves the installed packages and repos if you are using Fedora Linux.

## Usage
To use this you would either schedule its run it with a cronjob or do it yourself manually.
You need to provide an argument for the backup storage location and it will
create the required folders within it.