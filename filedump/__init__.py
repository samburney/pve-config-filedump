import os
import sys
import argparse
import sqlite3


def main():
    args = parse_arguments()

    # Check specified files exist
    if os.path.isfile(args.input_file) is False:
        print(f'{args.input_file}: Does not exist or is not a normal file', file=sys.stderr)
        exit(1)

    if os.path.isdir(args.output_path) is False:
        # If missing, create it
        if os.path.exists(args.output_path) is False:
            os.mkdir(args.output_path)
        else:
            print(f'{args.output_path}: Already exists but is not a directory', file=sys.stderr)
            exit(1)

    # Open database
    conn = sqlite3.connect(args.input_file, detect_types=sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row

    # Build directory list
    c = conn.cursor()
    sql = "SELECT * FROM tree WHERE type = 4 ORDER BY inode ASC"
    result = c.execute(sql)

    dirs = {}
    if result is not None:
        for row in result.fetchall():
            dirs[row['inode']] = {
                'parent': row['parent'],
                'name': row['name'],
            }

    # Build file list
    c = conn.cursor()
    sql = "SELECT * FROM tree WHERE type = 8 ORDER BY inode ASC"
    result = c.execute(sql)

    files = {}
    if result is not None:
        for row in result.fetchall():
            files[row['inode']] = {
                'parent': row['parent'],
                'name': row['name'],
            }

    # Create directory tree in output folder
    for dir_id in dirs:
        dir = dirs[dir_id]
        dir_path = f'{args.output_path}{os.path.sep}{make_path(dir, dirs)}'

        if os.path.isdir(dir_path) is False:
            # If missing, create it
            if os.path.exists(dir_path) is False:
                os.mkdir(dir_path)
            else:
                print(f'{dir_path}: Already exists but is not a directory', file=sys.stderr)
                exit(1)

    # Create files
    for file_id in files:
        file = files[file_id]
        file_path = f'{args.output_path}{os.path.sep}{make_path(file, dirs)}'

        print(file_path)
        if os.path.isfile(file_path) is False:
            # Check path doesn't exist
            if os.path.exists(file_path) is True:
                print(f'{file_path}: Already exists but is not a file', file=sys.stderr)
                exit(1)

            # Write file
            with open(file_path, 'wb') as file:
                sql = f'SELECT data FROM tree WHERE inode = {file_id}'
                result = c.execute(sql)

                if result is not None:
                    file_content = result.fetchone()['data']

                    if file_content is not None:
                        file.write(file_content)
                        file.close()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Dump /etc/pve filestructure from Proxmox VE config.db')

    parser.add_argument('-o', '--output-path', help='Path to output directory', required=True)
    parser.add_argument('-i', '--input-file', help='Path to config.db file', required=True)

    args = parser.parse_args()

    return args


def make_path(file, dirs):
    path = file['name']

    parent_id = file['parent']
    while parent_id != 0:
        parent_name = dirs[parent_id]['name']
        path = f'{parent_name}{os.path.sep}{path}'

        parent_id = dirs[parent_id]['parent']

    return(path)


if __name__ == "__main__":
    main()
