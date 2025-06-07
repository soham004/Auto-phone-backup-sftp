import os
import stat
import paramiko
import time
import json

with open('creds.json', 'r') as f:
    config = json.load(f)

HOST = '192.168.0.100'
PORT = 8022
USERNAME = config.get('username', '')
PASSWORD = config.get('password', '')
REMOTE_ROOT = '/storage/emulated/0'
EXTENSIONS = [
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.svg',
    # Videos
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.m4v', '.ts'
]

def connect_sftp():
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USERNAME, password=PASSWORD)
    return paramiko.SFTPClient.from_transport(transport)

def list_tree(sftp, remote_dir, prefix="", file_counter=None):
    if file_counter is None:
        file_counter = [0]
    try:
        items = sftp.listdir_attr(remote_dir)
    except Exception as e:
        return False  # Don't print folders we can't access

    files = []
    folders = []
    for item in items:
        if stat.S_ISDIR(item.st_mode):
            folders.append(item)
        else:
            if any(item.filename.lower().endswith(ext) for ext in EXTENSIONS):
                files.append(item)
                file_counter[0] += 1

    # Recursively check subfolders
    folder_results = []
    for idx, folder in enumerate(folders):
        is_last = idx == len(folders) - 1 and not files
        sub_prefix = prefix + ("└── " if is_last else "├── ")
        sub_indent = prefix + ("    " if is_last else "│   ")
        has_files = list_tree(sftp, f"{remote_dir}/{folder.filename}", sub_indent, file_counter)
        folder_results.append((folder, sub_prefix, has_files))

    # Only print if this folder or any subfolder has files
    if files or any(has_files for _, _, has_files in folder_results):
        print(f"{prefix}{os.path.basename(remote_dir) if prefix else remote_dir}")
        for folder, sub_prefix, has_files in folder_results:
            if has_files:
                print(f"{sub_prefix}{folder.filename}")
        for idx, file in enumerate(files):
            is_last = idx == len(files) - 1
            print(f"{prefix}{'└──' if is_last else '├──'} {file.filename}")
        return True
    return False

def main():
    print("Connecting to phone via SFTP...")
    sftp = connect_sftp()
    print("Listing files with extension(s):", EXTENSIONS)
    file_counter = [0]
    start_time = time.time()
    list_tree(sftp, REMOTE_ROOT, file_counter=file_counter)
    print(f"\nTotal files detected: {file_counter[0]}")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    if sftp is not None:
        sftp.close()

if __name__ == "__main__":
    main()
