import subprocess
import os
import json

with open('creds.json') as f:
    config = json.load(f)

REMOTE_USER = config['username']
REMOTE_HOST = "192.168.119.244"
REMOTE_PORT = "8022"
REMOTE_ROOT = "/storage/emulated/0"
BACKUP_DIR = "./backup/"

EXTENSIONS = [
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.svg',
    # Files
    '.txt', '.pdf', '.docx', '.xlsx', '.pptx',
    # Audio
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma',
    # Videos
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.m4v', '.ts'
]

def build_rsync_patterns(extensions):
    patterns = ["--include=*/"]  # Always include directories!
    for ext in extensions:
        patterns.append(f'--include=*.{ext.lstrip(".")}')
    patterns.append('--exclude=*')
    return patterns

def backup_files():
    patterns = build_rsync_patterns(EXTENSIONS)
    rsync_cmd = [
        "rsync",
        "-av",  # archive, verbose, compress
        "--info=progress2",  # Show progress, speed, and ETA
        "-e", f"ssh -p {REMOTE_PORT}",
        *patterns,
        f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_ROOT}/",
        BACKUP_DIR
    ]
    print("Running rsync to backup media files with progress...")
    print(" ".join(rsync_cmd))
    subprocess.run(rsync_cmd)

if __name__ == "__main__":
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_files()