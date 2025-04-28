from .tray_icons import MainWindow
from .watchdog import watch_detach, convert_to_ico
from .config import load_config
from pathlib import Path


def main():
    c = load_config()
    _observer = None

    for config in c.icons:
        src = config.src
        dst = config.dst
        if not dst.exists():
            convert_to_ico(src, dst)
        _observer = watch_detach(src, dst)

    first_icon = Path(c.icons[0].dst)
    _w = MainWindow(icon_path=first_icon, krita_handler=_observer)
    print(f"Watching icon '{first_icon}' for changes...")
    _w.observer.start()
    _w.run()


if __name__ == "__main__":
    main()
