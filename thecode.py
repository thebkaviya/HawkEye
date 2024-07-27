import os
import time
import threading
import psutil
from ctypes import windll

# List of websites to block
BLOCKED_SITES = [
    "www.instagram.com",
    "ww.x.com",
    "www.espncricinfo.com",
    "www.formula1.com"
]
ablank = []
if BLOCKED_SITES != ablank:
    print("Sites Entered")

# Path to the hosts file
HOSTS_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts"

# Backup path for the hosts file
BACKUP_HOSTS_FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts_backup"

# String to be added to the hosts file to block websites
BLOCK_STRING = "127.0.0.1"

# Function to check if Zoom is running
def is_zoom_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == 'zoom.exe':
            return True
            print("Zoom running")
    return False
    

# Function to backup the hosts file
def backup_hosts_file():
    if not os.path.exists(BACKUP_HOSTS_FILE_PATH):
        os.rename(HOSTS_FILE_PATH, BACKUP_HOSTS_FILE_PATH)
        print("Hosts file backed up.")

# backup_hosts_file()

# Function to restore the hosts file from backup
def restore_hosts_file():
    if os.path.exists(BACKUP_HOSTS_FILE_PATH):
        os.rename(BACKUP_HOSTS_FILE_PATH, HOSTS_FILE_PATH)
        print("Hosts file restored. Blocking inactive.")

# Function to block websites by updating the hosts file
def block_websites():
    with open(HOSTS_FILE_PATH, 'a') as hosts_file:
        for site in BLOCKED_SITES:
            hosts_file.write(f"{BLOCK_STRING} {site}\n")
        print("Hosts file edited & updated. Blocking active.")

# Function to check for and manage site blocking
def manage_site_blocking():
    # Ensure the script runs with admin rights (necessary for modifying hosts file)
    try:
        windll.shell32.IsUserAnAdmin()
    except:
        print("Admin rights required. Please run the script as an administrator.")
        return

    while True:
        if is_zoom_running():
            if not os.path.exists(BACKUP_HOSTS_FILE_PATH):
                backup_hosts_file()
            block_websites()
        else:
            print("Zoom not running.")
            if os.path.exists(BACKUP_HOSTS_FILE_PATH):
                restore_hosts_file()
        
        print("---------------")
        time.sleep(10)  # Check every minute
        

# Function to run the blocking manager in a separate thread
def run_in_background():
    blocking_thread = threading.Thread(target=manage_site_blocking, daemon=True)
    blocking_thread.start()
    blocking_thread.join()

# Function to initialize and start the background thread
def start_background_thread():
    # Run the thread for site blocking
    background_thread = threading.Thread(target=run_in_background, daemon=True)
    background_thread.start()
    background_thread.join()
    print("Thread strated")

if __name__ == "__main__":
    start_background_thread()
