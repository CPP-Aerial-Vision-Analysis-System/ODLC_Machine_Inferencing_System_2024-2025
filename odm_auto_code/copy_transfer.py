import os
import time
import shutil

source_folder = r'/home/astra/ODLC_Machine_Inferencing_System_2024-2025/odm_auto_code/results'

destination_folder = r'/media/astra/ESD-USB/test_results'

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