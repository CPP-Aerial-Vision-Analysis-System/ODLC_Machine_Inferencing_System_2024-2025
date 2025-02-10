import os
import time
import shutil

source_folder = r'./results'

destination_folder = r'D:\test'

os.makedirs(destination_folder, exist_ok=True)

time.sleep(5)

try:
    shutil.copytree(source_folder,destination_folder, dirs_exist_ok=True)
    print(f"Results successfully copied to {destination_folder}")
except PermissionError as e:
    print(f"Permission error: {e}")
    print("Retrying in 5 seconds...")
    time.sleep(5)
    shutil.copytree(source_folder,destination_folder, dirs_exist_ok=True)