#!/bin/bash

# python --version
# python -c "import pyodm; print('PyODM is installed')"

pip show pyodm > /dev/null
if [ $? -ne 0 ]; then
    echo "pyodm not found, installing..."
    pip install pyodm
else
    echo "pyodm is already installed."
fi


echo "Starting execution..."

python main.py
sleep 5
python copy_transfer.py

echo "All Python scripts have finished running"