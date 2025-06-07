import subprocess
import os
import re
import time

# Edit these as needed
REMOTE_USER = "soham"
REMOTE_HOST = "192.168.0.100"
REMOTE_PORT = "8022"
REMOTE_ROOT = "/storage/emulated/0"

EXTENSIONS = [
    # Images
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.svg',
    # Videos
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.m4v', '.ts'
]

def build_rsync_patterns(extensions):
    patterns = ["--include=*/"]  # Always include directories!
    for ext in extensions:
        patterns.append(f'--include=*.{ext.lstrip(".")}')
    patterns.append('--exclude=*')
    return patterns

def run_rsync_and_get_files():
    patterns = build_rsync_patterns(EXTENSIONS)
    rsync_cmd = [
        "rsync",
        "-avzn",  # archive, verbose, dry-run, compress
        "-e", f"ssh -p {REMOTE_PORT}",
        *patterns,
        f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_ROOT}/",
        "./rsync_temp/"
    ]
    result = subprocess.run(rsync_cmd, capture_output=True, text=True)
    files = []
    for line in result.stdout.splitlines():
    # Skip summary/statistics lines
        if (
            not line
            or line.endswith('/')
            or line.startswith('sending')
            or line.startswith('receiving')
            or line.startswith('created')
            or line.startswith('sent ')
            or line.startswith('total size is')
            or line.startswith('speedup is')
        ):
            continue
        files.append(line.strip())
    return files

def build_tree(files):
    tree = {}
    for filepath in files:
        parts = filepath.split(os.sep)
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault('__files__', []).append(parts[-1])
    return tree

def print_tree(node, prefix=""):
    total = 0
    files = node.get('__files__', [])
    folders = [k for k in node.keys() if k != '__files__']
    if files or folders:
        if prefix == "":
            print(".")
        for idx, folder in enumerate(sorted(folders)):
            is_last = idx == len(folders) - 1 and not files
            sub_prefix = prefix + ("└── " if is_last else "├── ")
            sub_indent = prefix + ("    " if is_last else "│   ")
            print(f"{sub_prefix}{folder}")
            count = print_tree(node[folder], sub_indent)
            total += count
        for idx, file in enumerate(sorted(files)):
            is_last = idx == len(files) - 1
            print(f"{prefix}{'└──' if is_last else '├──'} {file}")
            total += 1
    return total

def main():
    start_time = time.time()
    print("Scanning remote files with rsync...")
    files = run_rsync_and_get_files()
    tree = build_tree(files)
    print("\nDetected files tree:")
    total = print_tree(tree)
    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    print(f"\nTotal files detected: {total}")

if __name__ == "__main__":
    main()