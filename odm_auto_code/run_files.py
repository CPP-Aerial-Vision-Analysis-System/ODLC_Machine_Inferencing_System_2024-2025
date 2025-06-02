import subprocess
import time
from odm_process import ODMProcessor
from copy_transfer import ResultsTransfer

processor = ODMProcessor()
try:
    processor.start_container()
    processor.process_images(
        image_folder=r'C:\Users\valde\Desktop\cs_classes\SUAS\ODLC_Machine_Inferencing_System_2024-2025\5-25-25_images\test_3',
        source_folder=r'C:\Users\valde\Desktop\cs_classes\SUAS\ODLC_Machine_Inferencing_System_2024-2025\odm_auto_code\results'
    )
finally:
    processor.stop_container()

custom_transfer = ResultsTransfer(
    source_folder=r'C:\Users\valde\Desktop\cs_classes\SUAS\ODLC_Machine_Inferencing_System_2024-2025\odm_auto_code\results',
    destination_folder=r'C:\Users\valde\Desktop\cs_classes\SUAS\ODLC_Machine_Inferencing_System_2024-2025\test',
    retry_delay=10
)

custom_transfer.transfer_files()