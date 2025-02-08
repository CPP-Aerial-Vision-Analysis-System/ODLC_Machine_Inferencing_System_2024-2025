import subprocess
import os
import sys
sys.path.append('..')

from pyodm import Node, exceptions

process = subprocess.Popen(["docker", "run", "-ti", "-p", "3000:3000", "opendronemap/nodeodm"])
print("Docker container started. Running in the background...")

node = Node("localhost", 3000)

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

        print("Task completed, downloading results...")

        # Retrieve results
        task.download_assets("./results")

        print("Assets saved in ./results (%s)" % os.listdir("./results"))

        # Restart task and compute DTM
        task.restart({'dtm': True})
        task.wait_for_completion()

        print("Task completed, downloading results...")

        task.download_assets("./results_with_dtm")

        print("Assets saved in ./results_with_dtm (%s)" % os.listdir("./results_with_dtm"))
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

Steps For: ODM Terminal

Download ODM and find its location ex: C:/Users/valde/Desktop/projects/

Make a "datasets" folder inside it and add whatever datasets you like.

define the dataset name ex: 'drone_dataset_brighton_beach-master'
'''