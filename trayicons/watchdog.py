import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from .find_krita import get_krita


def convert_to_ico(krita_filepath, output_dir="."):
    """Converts a Krita image to an ICO file."""
    try:
        krita = get_krita()
        subprocess.run(
            [krita, krita_filepath, "--export", "--export-filename", "my_image.png"],
            check=True,
        )
        print(f"Converted '{krita_filepath}' to '{ico_filepath}'")
    except Exception as e:
        print(f"Error converting '{krita_filepath}': {e}")


class KritaEventHandler(FileSystemEventHandler):
    """Handles file system events, specifically looking for Krita file changes."""

    def on_modified(self, event):
        if not event.is_directory and event.src_path.lower().endswith((".kra", ".krz")):
            print(f"Detected change in: {event.src_path}")
            convert_to_ico(event.src_path)


if __name__ == "__main__":
    path_to_watch = "."  # You can change this to the directory you want to monitor
    output_directory = "icons"  # Directory to save the generated ICO files

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    event_handler = KritaEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    print(f"Watching directory '{path_to_watch}' for changes in Krita files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Stopped watching.")
