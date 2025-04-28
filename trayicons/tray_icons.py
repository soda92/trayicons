import os

import win32api
import win32con
import win32gui
import winerror

from pathlib import Path
from sodatools import str_path

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.events import FileSystemEventHandler


class MainWindow:
    def __init__(self, icon_path: Path, krita_handler):
        self.icon_path = icon_path
        self.krita_handler = krita_handler

        class IconEventHandler(FileSystemEventHandler):
            """Handles file system events, specifically looking for Krita file changes."""

            def __init__(self, icon_file: Path):
                super().__init__()
                self.output_file = icon_file

            def on_modified(self1, event):
                if not event.is_directory and event.src_path.lower().endswith(
                    (".ico", ".krz")
                ):
                    print(f"Detected change in: {event.src_path}")
                    self.update_icons()

        def create_obeserver() -> BaseObserver:
            output_directory = self.icon_path.resolve().parent
            # Create the output directory if it doesn't exist
            os.makedirs(output_directory, exist_ok=True)

            event_handler = IconEventHandler(icon_file=self.icon_path)
            observer = Observer()
            observer.schedule(event_handler, self.icon_path.parent, recursive=False)
            return observer

        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated")
        message_map = {
            msg_TaskbarRestart: self.OnRestart,
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_USER + 20: self.OnTaskbarNotify,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # could also specify a wndproc.

        # Don't blow up if class already registered to make testing easier
        try:
            _classAtom = win32gui.RegisterClass(wc)
        except win32gui.error as err_info:
            if err_info.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            wc.lpszClassName,
            "Taskbar Demo",
            style,
            0,
            0,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            hinst,
            None,
        )
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()
        self.observer = create_obeserver()

    def update_icons(self):
        """Updates the icon in the system tray."""
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)
        iconPathName = str_path(self.icon_path)
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = None
            loaded = False
            while not loaded:
                try:
                    hicon = win32gui.LoadImage(
                        hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags
                    )
                except Exception as _e:
                    import time

                    time.sleep(0.1)
                    continue
                else:
                    loaded = True
        else:
            print("Can't find icon file")
            exit(-1)
            # hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "Python Demo")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
        except win32gui.error as e:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print(f"Failed to update tray icon: {e}")
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def _DoCreateIcons(self):
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)
        iconPathName = str_path(self.icon_path)
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(
                hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags
            )
        else:
            print("Can't find icon file")
            exit(-1)
            # hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "Python Demo")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print("Failed to add the taskbar icon - is explorer running?")
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            print("You clicked me.")
        elif lparam == win32con.WM_LBUTTONDBLCLK:
            print("You double-clicked me - goodbye")
            win32gui.DestroyWindow(self.hwnd)
            self.cleanup_handler()
        elif lparam == win32con.WM_RBUTTONUP:
            print("You right clicked me.")
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "Display Dialog")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "Say Hello")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "Exit program")
            pos = win32gui.GetCursorPos()
            # See https://learn.microsoft.com/en-us/windows/win32/api/_menurc/
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(
                menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None
            )
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == 1023:
            import win32gui_dialog  # type: ignore

            win32gui_dialog.DemoModal()
        elif id == 1024:
            print("Hello")
        elif id == 1025:
            print("Goodbye")
            win32gui.DestroyWindow(self.hwnd)
            self.cleanup_handler()
        else:
            print("Unknown command -", id)

    def cleanup_handler(self):
        self.krita_handler.stop()
        self.krita_handler.join()

    def run(self):
        win32gui.PumpMessages()
