from .tray_icons import MainWindow
from .watchdog import KritaFileWatcher, convert_to_ico
from .config import get_config_path, Config


def main():
    config_file = get_config_path()
    try:
        config_data = Config.from_toml(config_file)
    except ValueError as e:
        print(f"Error loading configuration: {e}")
        return

    if not config_data.icons:
        print("No icons configured in 'icons.toml'. Exiting.")
        return

    # A single watcher for all Krita source files.
    krita_watcher = KritaFileWatcher()

    for config in config_data.icons:
        src = config.src
        dst = config.dst
        if not dst.exists():
            convert_to_ico(src, dst)
        krita_watcher.add_watch(src, dst)

    tray_windows = []
    for config in config_data.icons:
        tray_window = MainWindow(icon_path=config.dst, krita_handler=krita_watcher)
        print(f"Watching icon '{config.dst}' for changes to update tray.")
        tray_window.observer.start()
        tray_windows.append(tray_window)

    # Run all tray windows
    for tray_window in tray_windows:
        tray_window.run()

if __name__ == "__main__":
    main()
