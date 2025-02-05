import subprocess

# Define the ODM docker command
cmd = [
    'docker', 'run', '-ti', '--rm', '-v', 'C:/Users/valde/Desktop/projects/ODM/datasets:/datasets', 'opendronemap/odm', '--project-path', '/datasets', 'drone_dataset_brighton_beach-master'
]

process = subprocess.run(cmd, capture_output=True, text=True)

print(process.stdout)
print(process.stderr)

'''
ODM results would be outputted to the same dataset folder that the images were taken from. Files are the same names

Steps:
Download ODM and find its location ex: C:/Users/valde/Desktop/projects/

Make a "datasets" folder inside it and add whatever datasets you like.

define the dataset name ex: 'drone_dataset_brighton_beach-master'
'''