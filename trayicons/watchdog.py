import os
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.events import FileSystemEventHandler
import subprocess
from .find_krita import get_krita
from sodatools import str_path
from pathlib import Path


def convert_to_ico(krita_filepath, output_file: Path):
    """Converts a Krita image to an ICO file."""
    try:
        krita = get_krita()
        subprocess.run(
            [
                str_path(krita),
                krita_filepath,
                "--export",
                "--export-filename",
                str_path(output_file),
            ],
            check=True,
        )
    except Exception as e:
        print(f"Error converting '{krita_filepath}': {e}")


class KritaEventHandler(FileSystemEventHandler):
    """Handles file system events, specifically looking for Krita file changes."""

    def __init__(self, output_file: Path):
        super().__init__()
        self.output_file = output_file

    def on_modified(self, event):
        if not event.is_directory and event.src_path.lower().endswith((".kra", ".krz")):
            print(f"Detected change in: {event.src_path}")
            convert_to_ico(event.src_path, self.output_file)


def watch_detach(path_to_watch: Path, output_file: Path) -> BaseObserver:
    output_directory = output_file.resolve().parent
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    event_handler = KritaEventHandler(output_file=output_file)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch.parent, recursive=False)
    observer.start()
    print(f"Watching directory '{path_to_watch}' for changes in Krita files...")
    return observer
