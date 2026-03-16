"""Main application class."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, GLib, Gtk

from lexiscan import APP_ID, APP_NAME
from lexiscan.utils.i18n import _
from lexiscan.clipboard.monitor import ClipboardMonitor
from lexiscan.hotkeys.listener import HotkeyListener
from lexiscan.lookup.aggregator import LookupAggregator
from lexiscan.window import LexiScanWindow


class LexiScanApp(Adw.Application):
    """Main LexiScan application."""

    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.window = None
        self.clipboard_monitor = None
        self.hotkey_listener = None
        self.aggregator = LookupAggregator()
        self._active = True

    def do_startup(self):
        Adw.Application.do_startup(self)
        self._load_css()
        self._setup_actions()

    def do_activate(self):
        if not self.window:
            self.window = LexiScanWindow(application=self)
            self.window.set_title(APP_NAME)

        self._start_clipboard_monitor()
        self._start_hotkey_listener()
        self.window.present()

    def _load_css(self):
        """Load custom CSS stylesheet."""
        import os
        css_path = os.path.join(os.path.dirname(__file__), "..", "data", "style.css")
        if os.path.exists(css_path):
            provider = Gtk.CssProvider()
            provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_display(
                self.window.get_display() if self.window else
                __import__("gi.repository.Gdk", fromlist=["Gdk"]).Gdk.Display.get_default(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

    def _setup_actions(self):
        """Register application actions."""
        toggle_action = Gio.SimpleAction.new("toggle-overlay", None)
        toggle_action.connect("activate", self._on_toggle_overlay)
        self.add_action(toggle_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self._on_quit)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Control>q"])

        lookup_action = Gio.SimpleAction.new("lookup", GLib.VariantType.new("s"))
        lookup_action.connect("activate", self._on_lookup)
        self.add_action(lookup_action)

    def _start_clipboard_monitor(self):
        """Start monitoring X11 clipboard selections."""
        if self.clipboard_monitor is None:
            self.clipboard_monitor = ClipboardMonitor(self._on_text_selected)
            self.clipboard_monitor.start()

    def _start_hotkey_listener(self):
        """Start global hotkey listener."""
        if self.hotkey_listener is None:
            self.hotkey_listener = HotkeyListener(
                toggle_callback=self._toggle_from_hotkey,
                lookup_callback=self._force_lookup_from_hotkey,
            )
            self.hotkey_listener.start()

    def _on_text_selected(self, text):
        """Called when user selects text anywhere on screen."""
        if not self._active:
            return
        text = text.strip()
        if text and len(text) < 100:
            self._do_lookup(text)

    def _do_lookup(self, word):
        """Perform dictionary lookup and display results."""
        if self.window:
            self.window.show_loading(word)
            self.aggregator.lookup(word, callback=self._on_results)

    def _on_results(self, result):
        """Called when lookup results are ready."""
        GLib.idle_add(self._update_ui, result)

    def _update_ui(self, result):
        if self.window:
            self.window.show_results(result)
        return False

    def _on_toggle_overlay(self, action, param):
        self._active = not self._active
        if self.window:
            if self._active:
                self.window.present()
            else:
                self.window.hide()

    def _toggle_from_hotkey(self):
        GLib.idle_add(self._on_toggle_overlay, None, None)

    def _force_lookup_from_hotkey(self):
        """Force lookup of current clipboard content."""
        def do_lookup():
            if self.clipboard_monitor:
                text = self.clipboard_monitor.get_current_text()
                if text:
                    self._on_text_selected(text)
            return False
        GLib.idle_add(do_lookup)

    def _on_lookup(self, action, param):
        word = param.get_string()
        if word:
            self._do_lookup(word)

    def _on_quit(self, action, param):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        if self.clipboard_monitor:
            self.clipboard_monitor.stop()
        self.quit()

    def do_shutdown(self):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        if self.clipboard_monitor:
            self.clipboard_monitor.stop()
        Adw.Application.do_shutdown(self)
