# pve-config-filedump
Dump config files in a Proxmox VE config.db to a directory

## Installation
```
git clone https://github.com/samburney/pve-config-filedump
cd pve-config-filedump
pip3 install -e .
```

## Usage
```
$ pve-config-filedump -h
usage: pve-config-filedump [-h] -o OUTPUT_PATH -i INPUT_FILE

Dump /etc/pve filestructure from Proxmox VE config.db

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Path to output directory
  -i INPUT_FILE, --input-file INPUT_FILE
                        Path to config.db file
```
