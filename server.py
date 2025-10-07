from http.server import HTTPServer, SimpleHTTPRequestHandler
import builder
import time
import threading
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
            if path.startswith(ignore_dir):
                return True
        return False

    def on_modified(self, event):
        if not self._should_ignore(event.src_path):
            print(f"Rebuilt site.")
            self.callback(*self.args, **self.kwargs) # Calls the callback function if the directory is modified


def start_server(directory, port):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    server = HTTPServer(('localhost', port), Handler)

    print(f"Serving '{directory}' at http://localhost:{port}")
    server.serve_forever()


def serve_site(site_dir, dest_dir, port):

    builder.build_site(site_dir, dest_dir) # Build the site once to start
    print(f"Building site to {dest_dir}")

    event_handler = DiffHandler(builder.build_site, [dest_dir], site_dir, dest_dir) # Create an event handler with the build function as a callback
    observer = Observer()
    observer.schedule(event_handler, site_dir, recursive=True) # Create the observer to watch for changes to the directory
    observer.start()

    server_thread = threading.Thread(target=start_server, args=(dest_dir, port), daemon=True)
    server_thread.start()

    try:
        while True:
            time.sleep(1) # Wait briefly each time to not be annoying

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
