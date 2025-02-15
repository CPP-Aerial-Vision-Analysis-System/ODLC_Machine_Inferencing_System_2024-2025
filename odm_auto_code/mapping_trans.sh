#!/bin/bash
echo "Starting execution..."

python main.py
sleep 5
python copy_transfer.py

echo "All Python scripts have finished running"