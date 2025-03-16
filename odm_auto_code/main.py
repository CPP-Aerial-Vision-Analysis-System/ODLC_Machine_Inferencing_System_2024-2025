import subprocess
import os
import sys
import time
sys.path.append('..')

from pyodm import Node, exceptions


# running this process would require wiping past docker containers that have the same name nodeodm
# process = subprocess.Popen(
#     ["docker", "run", "-d", "--name", "nodeodm", "-p", "3000:3000", "opendronemap/nodeodm"],
# )

# Start the container and capture its ID
process = subprocess.Popen(
    ["docker", "run", "-d", "-p", "3000:3000", "opendronemap/nodeodm"],
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
image_folder = r'C:\Users\valde\Desktop\projects\ODM\datasets\drone_dataset_brighton_beach-master\images'

image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

try:
    if not image_paths:
        raise FileNotFoundError(f"No image files found in {image_folder}")

    print(f"Uploading {len(image_paths)} images...")

    # Start a task with all images in the folder
    task = node.create_task(image_paths, {'dsm': True, 'orthophoto-resolution': 4})
    print(task.info())

    try:
        # Wait for completion
        task.wait_for_completion()

        # Retrieve results 
        # IDEA: Make it an exception to allow the code to continue and close the container as this still produces results
        task.download_assets(source_folder)

    except OSError as e:
        if e.errno == 32: 
            print("Warning file in use, WinError 32 case")
            # print(f"Assets saved in {source_folder} (%s)" % os.listdir(source_folder))

            # print("Task completed, downloading results...")
    except exceptions.TaskFailedError as e:
        print("\n".join(task.output()))
except exceptions.NodeConnectionError as e:
    print("Cannot connect: %s" % e)
except exceptions.NodeResponseError as e:
    print("Error: %s" % e)
except FileNotFoundError as e:
    print(e)

# stop container first before transferring files
print(f"stopping docker container {container_id}...")
subprocess.run(['docker', 'stop', container_id])

'''
ODM results would be outputted to the same dataset folder that the images were taken from. Files are the same names

Steps For: PyODM Version
pip install -U pyodm
Change the image_folder location

'''