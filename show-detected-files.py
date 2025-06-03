import os
import stat
import paramiko

# ===== CONFIGURATION =====
HOST = '192.168.119.244'
PORT = 22
USERNAME = ''
PASSWORD = ''
REMOTE_ROOT = '/storage/emulated/0'
EXTENSIONS = [
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.svg',
    # Videos
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.m4v', '.ts'
]
# ==========================

def connect_sftp():
    transport = paramiko.Transport((HOST, PORT))
    transport.connect(username=USERNAME, password=PASSWORD)
    return paramiko.SFTPClient.from_transport(transport)

def list_tree(sftp, remote_dir, prefix=""):
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

    # Recursively check subfolders
    folder_results = []
    for idx, folder in enumerate(folders):
        is_last = idx == len(folders) - 1 and not files
        sub_prefix = prefix + ("└── " if is_last else "├── ")
        sub_indent = prefix + ("    " if is_last else "│   ")
        has_files = list_tree(sftp, f"{remote_dir}/{folder.filename}", sub_indent)
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
    list_tree(sftp, REMOTE_ROOT)
    if sftp is not None:
        sftp.close()

if __name__ == "__main__":
    main()
