import subprocess
import time
from odm_process import ODMProcessor
from copy_transfer import ResultsTransfer

processor = ODMProcessor()
try:
    processor.start_container()
    processor.process_images(
        image_folder=r'C:\Users\valde\Desktop\CS classes\senior_projects\ODLC_Machine_Inferencing_System_2024-2025\Phalaborwa_sm\Phalaborwa_5530',
        source_folder=r'C:\Users\valde\Desktop\CS classes\senior_projects\ODLC_Machine_Inferencing_System_2024-2025\results'
    )
finally:
    processor.stop_container()

custom_transfer = ResultsTransfer(
    source_folder=r'C:\Users\valde\Desktop\CS classes\senior_projects\ODLC_Machine_Inferencing_System_2024-2025\results',
    destination_folder=r'C:\Users\valde\Desktop\CS classes\senior_projects\ODLC_Machine_Inferencing_System_2024-2025\odm_auto_code\test',
    retry_delay=10
)
custom_transfer.transfer_files()