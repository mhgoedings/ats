# brew install libyaml
# pip install watchdog

# pip uninstall watchdog
# cd ~/Downloads
# git clone git://github.com/gorakhargosh/watchdog.git
# cd watchdog
# python setup.py install

# watchmedo log --debug-force-fsevents --patterns="*.py;*.txt" --ignore-directories --recursive ~/

#!/usr/bin/python
import time
#from watchdog.observers import Observer
from watchdog.observers.fsevents import FSEventsObserver as Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/data/', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
