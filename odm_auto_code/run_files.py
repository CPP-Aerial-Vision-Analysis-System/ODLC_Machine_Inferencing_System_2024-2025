import subprocess
import time
from odm_process import ODMProcessor
from copy_transfer import ResultsTransfer

def run_mapping():
    processor = ODMProcessor()
    try:
        processor.start_container()
        processor.process_images(
            image_folder=r'/home/astra/ODLC_Machine_Inferencing_System_2024-2025/odm_auto_code/datasets/drone_dataset_brighton_beach/images',
            source_folder=r'./results'
        )
    finally:
        processor.stop_container()

    custom_transfer = ResultsTransfer(
        source_folder=r'/home/astra/ODLC_Machine_Inferencing_System_2024-2025/odm_auto_code/results',
        destination_folder=r'/media/astra/ESD-USB/test_results',
        retry_delay=10
    )
    custom_transfer.transfer_files()