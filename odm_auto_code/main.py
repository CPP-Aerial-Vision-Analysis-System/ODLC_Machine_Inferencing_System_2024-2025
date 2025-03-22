import subprocess
import os
import sys
import time
sys.path.append('..')

print("fuck you, FUCK YOU")

from pyodm import Node, exceptions

# running this process would require wiping past docker containers that have the same name nodeodm
# process = subprocess.Popen(
#     ["docker", "run", "-d", "--name", "nodeodm", "-p", "3000:3000", "opendronemap/nodeodm"],
# )

# Start the container and capture its ID
process = subprocess.Popen(
    ["docker", "run", "--runtime", "nvidia", "-d", "-p", "3000:3000", "opendronemap/nodeodm"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
container_id, error = process.communicate()

if error:
    print(f"Error starting container: {error.decode()}")
    exit(1)

# Decode container ID from bytes to string and strip any extra whitespace
container_id = container_id.decode().strip()
print(f"Docker container started with ID: {container_id}")

# Wait for the container to be fully initialized
time.sleep(10)  

node = Node("localhost", 3000)

# Results path
source_folder = r'./results'

# add proper jetson directory here
image_folder = r'/home/astra/ODLC_Machine_Inferencing_System_2024-2025/odm_auto_code/datasets/drone_dataset_brighton_beach/images'

image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

try:
    if not image_paths:
        raise FileNotFoundError(f"No image files found in {image_folder}")

    print(f"Uploading {len(image_paths)} images...")

    # Start a task with all images in the folder

    # dsm : Build a digital surface model, ground + objects
    # orthophoto-resolution: cm / pixel, capped by ground sampling distance

    task = node.create_task(image_paths, {'dsm': True, 'orthophoto-resolution': 2, 'pc-quality': 'low', 'fast-orthophoto' : True})
    print(task.info())

    try:
        # Wait for completion
        task.wait_for_completion()

        print("Task completed, downloading results...")

        # Retrieve results 
        task.download_assets(source_folder)

        # print(f"Assets saved in {source_folder} (%s)" % os.listdir(source_folder))


        # stop container first before transferring files
        print(f"stopping docker container {container_id}...")
        subprocess.run(['docker', 'stop', container_id])
        # still closed it apparently
        # produce connection aborted error (ConnectionAbortedError(10053...))

        print("Task completed, downloading results...")

    except exceptions.TaskFailedError as e:
        print("\n".join(task.output()))
except exceptions.NodeConnectionError as e:
    print("Cannot connect: %s" % e)
except exceptions.NodeResponseError as e:
    print("Error: %s" % e)
except FileNotFoundError as e:
    print(e)


# ---------------------------------------
# # Define the ODM docker command
# cmd = [
#     'docker', 'run', '-ti', '--rm', '-v', 'C:/Users/valde/Desktop/projects/ODM/datasets:/datasets', 'opendronemap/odm', '--project-path', '/datasets', 'drone_dataset_brighton_beach-master'
# ]

# process = subprocess.run(cmd, capture_output=True, text=True)

# print(process.stdout)
# print(process.stderr)

'''
ODM results would be outputted to the same dataset folder that the images were taken from. Files are the same names

Steps For: PyODM Version
pip install -U pyodm
Change the image_folder location

'''