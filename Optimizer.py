import threading
import time
import random
import pygmo as pg
import numpy as np

class MultiThreadMotorBuilder:
    def __init__(self, total_files=100, concurrency_limit=3, batch_size=9):
        """
        :param total_files:      Total number of files to process
        :param concurrency_limit:Max number of simultaneous downloads
        :param batch_size:       Number of files to download in each batch 
        """
        self.total_files = total_files
        self.concurrency_limit = concurrency_limit
        self.batch_size = batch_size

        # For storing file contents
        self.results = [""] * total_files

        # We'll use an Event to signal that the password has been found
        self.found_password_event = threading.Event()

        # A lock to protect shared data (writing to self.results)
        self.results_lock = threading.Lock()

    def download_file(self, file_index: int) -> str:
        """
        Simulated download function.
        
        In a real scenario, replace this method with actual file reading
        or network download logic. Right now, it just sleeps 0.1-0.5s
        and returns dummy content with the "password" in file #42.
        """
        sleep_time = 0.1 + (random.random() * 0.4)
        time.sleep(sleep_time)

        if file_index == 42:
            return "This file contains the password!"
        return f"Dummy content for file index {file_index}"

    def worker_download(self, file_index: int):
        """
        Worker thread function:
          1) Check if we've already found the password; if so, return early.
          2) Otherwise, download the file content.
          3) Store the content in self.results.
          4) If the content has the 'password', set the found_password_event.
        """
        if self.found_password_event.is_set():
            return  # Skip if password is already found

        content = self.download_file(file_index)

        # Safely store the content in the results list
        with self.results_lock:
            self.results[file_index] = content

        # Check for the password
        if "password" in content.lower():
            self.found_password_event.set()

    def start_download(self):
        """
        Main method to coordinate:
          - Batches of `self.batch_size` files
          - Up to `self.concurrency_limit` threads at once
          - Early stop when password is found
        """
        for start_index in range(0, self.total_files, self.batch_size):
            if self.found_password_event.is_set():
                # Password found in a previous batch
                break

            end_index = min(start_index + self.batch_size, self.total_files)

            # We'll gather threads here
            threads = []

            for file_index in range(start_index, end_index):
                # If password is already found, skip launching more threads
                if self.found_password_event.is_set():
                    break

                t = threading.Thread(target=self.worker_download,
                                     args=(file_index,))
                t.start()
                threads.append(t)

                # If we've hit the concurrency limit, join on those threads
                if len(threads) == self.concurrency_limit:
                    for thr in threads:
                        thr.join()
                    threads.clear()

            # Join any remaining threads in this batch
            for thr in threads:
                thr.join()

            # "Batch analysis" - we can do deeper checks here if needed.
            # We'll just check the event, which is set in worker_download().
            if self.found_password_event.is_set():
                print(f"[Batch {start_index // self.batch_size}] Password found! Stopping early.")
                break
            else:
                print(f"[Batch {start_index // self.batch_size}] Files {start_index} to {end_index - 1} done. No password found.")

        if self.found_password_event.is_set():
            print("\nPassword file found!")
        else:
            print("\nPassword not found in any file.")

def main():
    downloader = MultiThreadMotorBuilder(total_files=100, concurrency_limit=3, batch_size=9)
    downloader.start_download()

if __name__ == "__main__":
    main()
