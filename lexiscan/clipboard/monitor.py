"""X11 clipboard monitoring for text selections."""

import threading
import subprocess

from gi.repository import GLib


class ClipboardMonitor:
    """Monitors X11 PRIMARY selection for text changes."""

    def __init__(self, callback, poll_interval_ms=500):
        self._callback = callback
        self._poll_interval_ms = poll_interval_ms
        self._last_text = ""
        self._running = False
        self._source_id = None

    def start(self):
        """Start polling the PRIMARY selection."""
        self._running = True
        self._source_id = GLib.timeout_add(
            self._poll_interval_ms, self._poll_selection
        )

    def stop(self):
        """Stop polling."""
        self._running = False
        if self._source_id is not None:
            GLib.source_remove(self._source_id)
            self._source_id = None

    def get_current_text(self):
        """Get current PRIMARY selection text."""
        return self._last_text

    def _poll_selection(self):
        """Poll the X11 PRIMARY selection via xclip."""
        if not self._running:
            return False

        thread = threading.Thread(target=self._read_selection, daemon=True)
        thread.start()
        return True  # Keep polling

    def _read_selection(self):
        """Read PRIMARY selection in background thread."""
        try:
            result = subprocess.run(
                ["xclip", "-selection", "primary", "-o"],
                capture_output=True,
                text=True,
                timeout=2,
            )
            text = result.stdout.strip() if result.returncode == 0 else ""
        except (FileNotFoundError, subprocess.TimeoutExpired):
            try:
                result = subprocess.run(
                    ["xsel", "--primary", "--output"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                text = result.stdout.strip() if result.returncode == 0 else ""
            except (FileNotFoundError, subprocess.TimeoutExpired):
                text = ""

        if text and text != self._last_text:
            self._last_text = text
            GLib.idle_add(self._callback, text)
