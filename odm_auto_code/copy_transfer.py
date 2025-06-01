import os
import time
import shutil
from pathlib import Path

class ResultsTransfer:
    def __init__(self, source_folder='./results', destination_folder='D:/test_results', retry_delay=5):
        self.source_folder = Path(source_folder)
        self.destination_folder = Path(destination_folder)
        self.retry_delay = retry_delay

    def setup_destination(self):
        """Create destination folder if it doesn't exist"""
        os.makedirs(self.destination_folder, exist_ok=True)

    def transfer_files(self):
        """Transfer files individually with progress tracking"""
        self.setup_destination()
        
        try:
            # Get list of files to transfer
            files_to_copy = []
            for root, _, files in os.walk(self.source_folder):
                for file in files:
                    src_path = Path(root) / file
                    rel_path = src_path.relative_to(self.source_folder)
                    dst_path = self.destination_folder / rel_path
                    files_to_copy.append((src_path, dst_path))

            total_files = len(files_to_copy)
            print(f"Starting transfer of {total_files} files...")

            # Copy files individually
            for idx, (src, dst) in enumerate(files_to_copy, 1):
                try:
                    # Create destination directory if needed
                    os.makedirs(dst.parent, exist_ok=True)
                    
                    # Copy with retry logic
                    self._copy_with_retry(src, dst)
                    
                    # Show progress
                    print(f"Copied {idx}/{total_files}: {src.name}")
                
                except Exception as e:
                    print(f"Error copying {src.name}: {e}")
                    continue

            print(f"Transfer completed to {self.destination_folder}")
            return True

        except Exception as e:
            print(f"Transfer failed: {e}")
            return False

    def _copy_with_retry(self, src, dst, max_retries=3):
        """Copy a single file with retry logic"""
        for attempt in range(max_retries):
            try:
                shutil.copy2(src, dst)
                return True
            except PermissionError as e:
                if attempt < max_retries - 1:
                    print(f"Permission error copying {src.name}, retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise
        return False

if __name__ == '__main__':
    transfer = ResultsTransfer()
    transfer.transfer_files()