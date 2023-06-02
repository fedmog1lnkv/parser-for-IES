# from ftplib import FTP

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

paths = ["BRG_PATH", "PUSK_PATH", "XDM_PATH"]


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        pass  # TODO: run    "./data_to_db.data_to_db(event.src_path)"   from this function


if __name__ == "__main__":
    observer = Observer()
    threads = []

    for i in range(len(paths)):
        event_handler = MyHandler()
        observer.schedule(event_handler, paths[i], recursive=True)
        threads.append(observer)

    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
