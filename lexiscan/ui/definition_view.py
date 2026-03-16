"""Widget for displaying word definitions."""

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from lexiscan.utils.i18n import _


class DefinitionView(Gtk.Box):
    """Displays a list of word definitions."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self._title = Gtk.Label(label=_("Definitioner"))
        self._title.add_css_class("heading")
        self._title.set_halign(Gtk.Align.START)
        self.append(self._title)

        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.append(self._container)
        self.set_visible(False)

    def update(self, definitions):
        """Update the view with new definitions."""
        # Clear existing
        while child := self._container.get_first_child():
            self._container.remove(child)

        if not definitions:
            self.set_visible(False)
            return

        self.set_visible(True)
        for defn in definitions[:8]:  # Limit display
            card = self._create_definition_card(defn)
            self._container.append(card)

    def _create_definition_card(self, defn):
        """Create a card widget for a single definition."""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        card.add_css_class("card")
        card.set_margin_start(4)
        card.set_margin_end(4)

        # Part of speech + language
        if defn.part_of_speech:
            pos_label = Gtk.Label(label=defn.part_of_speech)
            pos_label.add_css_class("dim-label")
            pos_label.add_css_class("caption")
            pos_label.set_halign(Gtk.Align.START)
            pos_label.set_margin_start(8)
            pos_label.set_margin_top(8)
            card.append(pos_label)

        # Meaning
        if defn.meaning:
            meaning_label = Gtk.Label(label=defn.meaning)
            meaning_label.set_wrap(True)
            meaning_label.set_halign(Gtk.Align.START)
            meaning_label.set_margin_start(8)
            meaning_label.set_margin_end(8)
            meaning_label.set_margin_top(4)
            card.append(meaning_label)

        # Example
        if defn.example:
            example_label = Gtk.Label(label=f"\u201c{defn.example}\u201d")
            example_label.set_wrap(True)
            example_label.add_css_class("dim-label")
            example_label.set_halign(Gtk.Align.START)
            example_label.set_margin_start(8)
            example_label.set_margin_end(8)
            card.append(example_label)

        # Synonyms
        if defn.synonyms:
            syn_text = _("Synonymer: ") + ", ".join(defn.synonyms)
            syn_label = Gtk.Label(label=syn_text)
            syn_label.set_wrap(True)
            syn_label.add_css_class("caption")
            syn_label.set_halign(Gtk.Align.START)
            syn_label.set_margin_start(8)
            syn_label.set_margin_end(8)
            syn_label.set_margin_bottom(8)
            card.append(syn_label)
        else:
            # Add bottom margin to last element
            last = card.get_last_child()
            if last:
                last.set_margin_bottom(8)

        return card
