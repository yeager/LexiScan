"""Global hotkey listener using pynput."""

import threading


class HotkeyListener:
    """Listens for global keyboard shortcuts."""

    def __init__(self, toggle_callback=None, lookup_callback=None):
        self._toggle_callback = toggle_callback
        self._lookup_callback = lookup_callback
        self._listener = None
        self._thread = None

    def start(self):
        """Start listening for hotkeys in a background thread."""
        try:
            from pynput import keyboard

            hotkeys = {}
            if self._toggle_callback:
                hotkeys["<ctrl>+<shift>+d"] = self._toggle_callback
            if self._lookup_callback:
                hotkeys["<ctrl>+<shift>+l"] = self._lookup_callback

            if hotkeys:
                self._listener = keyboard.GlobalHotKeys(hotkeys)
                self._listener.daemon = True
                self._listener.start()
        except ImportError:
            print("pynput not available - hotkeys disabled")
        except Exception as e:
            print(f"Could not start hotkey listener: {e}")

    def stop(self):
        """Stop the hotkey listener."""
        if self._listener:
            self._listener.stop()
            self._listener = None
