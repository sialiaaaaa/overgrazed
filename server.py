import builder
import time
import threading
import os
from validator import is_ignored_filename
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DiffHandler(FileSystemEventHandler):
    def __init__(self, callback, ignore_dirs=None, *args, **kwargs): # Implementation that accepts a callback function and arguments
        super().__init__()
        self.callback = callback
        self.ignore_dirs = ignore_dirs or []
        self.args = args
        self.kwargs = kwargs

    def _should_ignore(self, path): # Determines if a file is within an ignored directory
        for ignore_dir in self.ignore_dirs:
            if path.startswith(ignore_dir) or os.path.isdir(path):
                return True

        filename = os.path.basename(path) # Handle a bunch of common swapfiles
        if is_ignored_filename(filename):
            return True

        return False

    def on_modified(self, event):
        if not self._should_ignore(event.src_path):
            self.callback(*self.args, **self.kwargs) # Calls the callback function if the directory is modified


def start_server(directory, port):
    class Handler(SimpleHTTPRequestHandler): # Define a handler that acts in a specific directory
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    server = HTTPServer(('localhost', port), Handler) # Create a server with our handler

    print(f"Serving '{directory}' at http://localhost:{port}")
    server.serve_forever() # Serve it

def rebuild_site(site_dir, dest_dir):
    try:
        builder.build_site(site_dir, dest_dir)
        print(f"Rebuilt site to {dest_dir}")
    except Exception as e:
        print(f"Failed to rebuild site: {e}")

def serve_site(site_dir, dest_dir, port):

    try:
        builder.build_site(site_dir, dest_dir) # Build the site once to start
        print(f"Built site to {dest_dir}")
    except Exception as e:
        print(f"Failed to build site: {e}")

    event_handler = DiffHandler(rebuild_site, [dest_dir], site_dir, dest_dir) # Create an event handler with the build function as a callback
    observer = Observer()
    observer.schedule(event_handler, site_dir, recursive=True) # Create the observer to watch for changes to the directory
    observer.start()

    server_thread = threading.Thread(target=start_server, args=(dest_dir, port), daemon=True) # Create a thread to run start_server
    server_thread.start() # The server will end when the program does

    try:
        while True:
            time.sleep(1) # Wait briefly each time to not be annoying
    except KeyboardInterrupt:
        print(f"No longer serving site.")
    finally:
        observer.stop()
        observer.join()
