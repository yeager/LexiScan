"""Widget for displaying translations."""

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from lexiscan.utils.i18n import _


LANG_NAMES = {
    "sv": "Svenska",
    "en": "English",
    "de": "Deutsch",
    "fr": "Fran\u00e7ais",
}


class TranslationView(Gtk.Box):
    """Displays Swedish-English translations."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        self._title = Gtk.Label(label=_("\u00d6vers\u00e4ttning"))
        self._title.add_css_class("heading")
        self._title.set_halign(Gtk.Align.START)
        self.append(self._title)

        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.append(self._container)
        self.set_visible(False)

    def update(self, translations):
        """Update view with translation results."""
        while child := self._container.get_first_child():
            self._container.remove(child)

        if not translations:
            self.set_visible(False)
            return

        self.set_visible(True)
        seen = set()
        for trans in translations[:6]:
            key = (trans.source_word.lower(), trans.target_word.lower())
            if key in seen:
                continue
            seen.add(key)

            row = self._create_translation_row(trans)
            self._container.append(row)

    def _create_translation_row(self, trans):
        """Create a row showing a translation pair."""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.add_css_class("card")
        row.set_margin_start(4)
        row.set_margin_end(4)

        # Source
        src_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        src_box.set_hexpand(True)
        src_box.set_margin_start(8)
        src_box.set_margin_top(8)
        src_box.set_margin_bottom(8)

        src_lang = Gtk.Label(label=LANG_NAMES.get(trans.source_lang, trans.source_lang))
        src_lang.add_css_class("caption")
        src_lang.add_css_class("dim-label")
        src_lang.set_halign(Gtk.Align.START)
        src_box.append(src_lang)

        src_word = Gtk.Label(label=trans.source_word)
        src_word.set_halign(Gtk.Align.START)
        src_box.append(src_word)

        row.append(src_box)

        # Arrow
        arrow = Gtk.Label(label="\u2192")
        arrow.add_css_class("dim-label")
        arrow.set_valign(Gtk.Align.CENTER)
        row.append(arrow)

        # Target
        tgt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        tgt_box.set_hexpand(True)
        tgt_box.set_margin_end(8)
        tgt_box.set_margin_top(8)
        tgt_box.set_margin_bottom(8)

        tgt_lang = Gtk.Label(label=LANG_NAMES.get(trans.target_lang, trans.target_lang))
        tgt_lang.add_css_class("caption")
        tgt_lang.add_css_class("dim-label")
        tgt_lang.set_halign(Gtk.Align.START)
        tgt_box.append(tgt_lang)

        tgt_word = Gtk.Label(label=trans.target_word)
        tgt_word.set_halign(Gtk.Align.START)
        tgt_word.add_css_class("accent")
        tgt_box.append(tgt_word)

        row.append(tgt_box)

        if trans.part_of_speech:
            pos = Gtk.Label(label=trans.part_of_speech)
            pos.add_css_class("caption")
            pos.add_css_class("dim-label")
            pos.set_valign(Gtk.Align.CENTER)
            pos.set_margin_end(8)
            row.append(pos)

        return row
