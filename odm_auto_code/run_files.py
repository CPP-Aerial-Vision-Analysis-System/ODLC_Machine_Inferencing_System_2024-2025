import subprocess
import time

# Run the first script and wait for it to finish
print("Running first script...")
process1 = subprocess.Popen(["python", "main.py"])
process1.wait()  # Ensure it fully exits before continuing

# Add a delay to release file locks
time.sleep(5)

# Run the second script and wait
print("Running second script...")
process2 = subprocess.Popen(["python", "second_script.py"])
process2.wait()

print("Both scripts have finished executing!")

# currently not functioning properly due to winError32, If this works it would be better just to merge to main.py