import os
import time
from datetime import datetime
from sec_edgar_downloader import Downloader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import multiprocessing
import signal
import sys
def download_filings():
    downloader = Downloader()
    downloader.get("8-K", "AAPL")
    print("Download process completed.")
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, stop_event):
        self.stop_event = stop_event
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".txt"):
            return
        filename = os.path.basename(event.src_path)
        try:
            filing_date_str = filename.split('_')[1]
            filing_date = datetime.strptime(filing_date_str, "%Y%m%d")
            if filing_date.year < 2020:
                print(f"Found a filing before 2020: {filename}. Aborting the download!")
                self.stop_event.set()
        except Exception as e:
            print(f"Error processing file {filename}: {e}")
def monitor_directory(stop_event):
    event_handler = FileEventHandler(stop_event)
    observer = Observer()
    observer.schedule(event_handler, path='sec-edgar-downloader/AAPL/8-K/', recursive=False)
    observer.start()
    try:
        while not stop_event.is_set():
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
def terminate_process(p):
    p.terminate()
    p.join()
if __name__ == "__main__":
    stop_event = multiprocessing.Event()
    monitor_process = multiprocessing.Process(target=monitor_directory, args=(stop_event,))
    monitor_process.start()
    download_process = multiprocessing.Process(target=download_filings)
    download_process.start()
    try:
        download_process.join()
    except Exception as e:
        print(f"Error: {e}")
        terminate_process(download_process)
    if stop_event.is_set():
        terminate_process(download_process)
    monitor_process.terminate()
    monitor_process.join()
