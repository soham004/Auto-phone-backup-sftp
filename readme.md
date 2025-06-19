# Auto Phone Backup

## About

**Auto Phone Backup** is a set of Python scripts that allow you to automatically detect and back up images, videos, audio, and document files from your Android phone to your computer using `rsync` over SSH. The scripts preserve the original folder structure and provide progress feedback during backup. This solution is ideal for users who want a reliable, scriptable, and efficient way to back up their mobile media and documents to a PC.

---

## Requirements

- **Android Phone** with [Termux](https://f-droid.org/packages/com.termux/) installed
- **rsync** and **openssh** installed in Termux on your phone
- **Python 3.7+** installed on your client (PC) computer
- **git** installed on your client computer (optional, for cloning the repo)
- **rsync** and **ssh** installed on your client computer
- **A Wi-Fi network** (preferably 5GHz for faster transfers)
- **A `creds.json` file** on your client computer with your SSH credentials

---

## Setup Process

### 1. Setting Up Termux on Android

- Install [Termux](https://f-droid.org/packages/com.termux/) from F-Droid.
- Open Termux and run:
  ```sh
  pkg update
  pkg install openssh rsync
  ```
- Start the SSH server in Termux:
  ```sh
  sshd
  ```
- Find your phone's IP address:
  ```sh
  ifconfig
  ```
  (Look for your Wi-Fi IP, e.g., `192.168.1.100`)

### 2. Setting Up SSH Key Authentication (Recommended)

- On your PC, generate an SSH key if you don't have one:
  ```sh
  ssh-keygen
  ```
- Copy your public key to your phone (replace `8022` and `user` with your port and username if different):
  ```sh
  ssh-copy-id -p 8022 user@192.168.1.100
  ```
  If `ssh-copy-id` is not available, manually append the contents of your `~/.ssh/id_rsa.pub` to `~/.ssh/authorized_keys` on your phone.

- Test passwordless SSH:
  ```sh
  ssh -p 8022 user@192.168.1.100
  ```
  You should be logged in without a password prompt.

### 3. Setting Up the Scripts on Your Computer

- Clone this repository or download the scripts:
  ```sh
  git clone https://github.com/yourusername/auto-phone-backup.git
  cd auto-phone-backup/rsync
  ```
- Install Python dependencies (if using progress bar):
  ```sh
  pip install tqdm
  ```
- Ensure `rsync` and `ssh` are installed on your PC. On Ubuntu/Debian:
  ```sh
  sudo apt install rsync openssh-client
  ```
  On Windows, use [WSL](https://docs.microsoft.com/en-us/windows/wsl/) or install via [Git for Windows](https://gitforwindows.org/).

### 4. Create the `creds.json` File

- In the project root, create a file named `creds.json`:
  ```json
  {
      "username": "anyname"
  }
  ```
  > **Note:** The username actually didn't matter during testing on an android device with termux. But it's still there because the script can be used to backup files from remote devices too.

---

## How to Customize and Run the Rsync Python Script

1. **Edit `backup.py`**  
   - You can customize the `EXTENSIONS` list to include any file types you want to back up.
   - Adjust `REMOTE_HOST`, `REMOTE_PORT`, and `REMOTE_ROOT` in your `creds.json` or directly in the script if needed.

2. **Run the Backup Script**
   ```sh
   python backup.py
   ```
   - The script will scan your phone and copy all matching files to the `./backup/` folder, preserving the folder structure.
   - Progress, speed, and ETA will be shown in the terminal.

3. **Tips for Best Results**
   - **Connect both your phone and PC to a fast Wi-Fi network** (preferably 5GHz) for optimal transfer speeds.
   - For large backups, ensure your phone stays awake and connected to Wi-Fi.
   - You can re-run the script anytime; only new or changed files will be copied.

---

## Note on SFTP Support

> **SFTP is not supported in this project due to slow transfer speeds on Android devices.**
>
> All backup and file detection operations are performed using `rsync` over SSH for maximum speed and reliability.
---

## License

MIT License

---

**Enjoy fast, reliable, and scriptable phone backups!**
