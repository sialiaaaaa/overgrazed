from pathlib import Path
import time
import threading

import builder
from validator import is_ignored_filename
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DiffHandler(FileSystemEventHandler):
    def __init__(self, callback, ignore_dirs=None, *args, **kwargs):
        super().__init__()
        self.callback = callback
        self.ignore_dirs = [Path(d) for d in (ignore_dirs or [])]
        self.args = args
        self.kwargs = kwargs

    def _should_ignore(self, path):
        path = Path(path)

        for ignore_dir in self.ignore_dirs:
            if path.is_relative_to(ignore_dir):
                return True

        if is_ignored_filename(path.name):
            return True

        return False

    def on_modified(self, event):
        if not self._should_ignore(event.src_path):
            self.callback(*self.args, **self.kwargs)


def start_server(directory, port):
    class Handler(SimpleHTTPRequestHandler): # Define a handler that acts in a specific directory
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    server = HTTPServer(('localhost', port), Handler) # Create a server with our handler

    print(f"Serving '{directory}' at http://localhost:{port}")
    server.serve_forever() # Serve it

def rebuild_site(site_path, dest_path):
    try:
        builder.build_site(site_path, dest_path)
        print(f"Rebuilt site to {dest_path}")
    except Exception as e:
        print(f"Failed to rebuild site: {e}")

def serve_site(site_path, dest_path, port):

    try:
        builder.build_site(site_path, dest_path) # Build the site once to start
        print(f"Built site to {dest_path}")
    except Exception as e:
        print(f"Failed to build site: {e}")

    event_handler = DiffHandler(rebuild_site, [dest_path], site_path, dest_path) # Create an event handler with the build function as a callback
    observer = Observer()
    observer.schedule(event_handler, site_path, recursive=True) # Create the observer to watch for changes to the directory
    observer.start()

    server_thread = threading.Thread(target=start_server, args=(dest_path, port), daemon=True) # Create a thread to run start_server
    server_thread.start() # The server will end when the program does

    try:
        while True:
            time.sleep(1) # Wait briefly each time to not be annoying
    except KeyboardInterrupt:
        print(f"No longer serving site.")
    finally:
        observer.stop()
        observer.join()
