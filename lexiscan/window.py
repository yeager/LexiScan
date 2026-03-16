"""Main overlay window for LexiScan."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gdk, GLib, Gtk

from lexiscan.utils.i18n import _
from lexiscan.ui.definition_view import DefinitionView
from lexiscan.ui.phonetic_view import PhoneticView
from lexiscan.ui.image_view import ImageView
from lexiscan.ui.translation_view import TranslationView


class LexiScanWindow(Adw.ApplicationWindow):
    """Floating overlay window that shows dictionary results."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(420, 500)
        self.set_resizable(True)

        # Header bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        self.search_label = Gtk.Label(label=_("LexiScan - Ordbok"))
        self.search_label.add_css_class("title-4")
        header.set_title_widget(self.search_label)

        # Toggle monitoring button
        self.toggle_btn = Gtk.ToggleButton()
        self.toggle_btn.set_icon_name("system-search-symbolic")
        self.toggle_btn.set_active(True)
        self.toggle_btn.set_tooltip_text(_("Aktivera/avaktivera urklippsövervakning"))
        self.toggle_btn.connect("toggled", self._on_toggle_monitoring)
        header.pack_start(self.toggle_btn)

        # Manual search entry
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        search_box.set_margin_start(12)
        search_box.set_margin_end(12)
        search_box.set_margin_top(6)
        search_box.set_margin_bottom(6)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(_("Search ord..."))
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("activate", self._on_search_activate)
        search_box.append(self.search_entry)

        # Content area with scrolling
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_vexpand(True)

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.content_box.set_margin_start(12)
        self.content_box.set_margin_end(12)
        self.content_box.set_margin_top(6)
        self.content_box.set_margin_bottom(12)

        # Sub-views
        self.definition_view = DefinitionView()
        self.phonetic_view = PhoneticView()
        self.image_view = ImageView()
        self.translation_view = TranslationView()

        self.content_box.append(self.phonetic_view)
        self.content_box.append(self.definition_view)
        self.content_box.append(self.translation_view)
        self.content_box.append(self.image_view)

        self.scroll.set_child(self.content_box)

        # Loading spinner
        self.spinner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.spinner_box.set_valign(Gtk.Align.CENTER)
        self.spinner_box.set_vexpand(True)
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(48, 48)
        self.loading_label = Gtk.Label(label=_("Söker..."))
        self.loading_label.add_css_class("dim-label")
        self.spinner_box.append(self.spinner)
        self.spinner_box.append(self.loading_label)

        # Status label for empty state
        self.status_label = Gtk.Label(
            label=_("Select text i valfri app för att slå upp ord.\n\nKortkommando: Ctrl+Shift+D")
        )
        self.status_label.set_wrap(True)
        self.status_label.set_justify(Gtk.Justification.CENTER)
        self.status_label.add_css_class("dim-label")
        self.status_label.set_valign(Gtk.Align.CENTER)
        self.status_label.set_vexpand(True)

        # Stack to switch between states
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.add_named(self.status_label, "empty")
        self.stack.add_named(self.spinner_box, "loading")
        self.stack.add_named(self.scroll, "results")

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(header)
        main_box.append(search_box)
        main_box.append(self.stack)

        self.set_content(main_box)
        self.stack.set_visible_child_name("empty")

        # Keyboard shortcuts
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(key_controller)

    def show_loading(self, word):
        """Show loading state for a word lookup."""
        self.search_label.set_label(f"LexiScan - {word}")
        self.search_entry.set_text(word)
        self.loading_label.set_label(_("Söker \'{word}\'...").format(word=word))
        self.spinner.start()
        self.stack.set_visible_child_name("loading")
        self.present()

    def show_results(self, result):
        """Display lookup results."""
        self.spinner.stop()

        if not result or result.is_empty():
            self.loading_label.set_label(
                _("Inga resultat hittades för \'{word}\'.").format(word=result.word if result else "")
            )
            self.stack.set_visible_child_name("loading")
            self.spinner.stop()
            return

        self.search_label.set_label(f"LexiScan - {result.word}")
        self.definition_view.update(result.definitions)
        self.phonetic_view.update(result.word, result.phonetics)
        self.translation_view.update(result.translations)
        self.image_view.update(result.images)
        self.stack.set_visible_child_name("results")

    def _on_search_activate(self, entry):
        """Manual search from entry."""
        text = entry.get_text().strip()
        if text:
            app = self.get_application()
            if app:
                app.activate_action("lookup", GLib.Variant.new_string(text))

    def _on_toggle_monitoring(self, button):
        """Toggle clipboard monitoring."""
        app = self.get_application()
        if app:
            app._active = button.get_active()

    def _on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.close()
            return True
        return False
