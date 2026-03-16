"""Widget for displaying phonetic information and audio playback."""

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from lexiscan.utils.i18n import _
from lexiscan.utils.audio import play_audio_url


class PhoneticView(Gtk.Box):
    """Displays word with phonetic transcription and audio button."""

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.set_margin_top(4)

        self._word_label = Gtk.Label()
        self._word_label.add_css_class("title-2")
        self._word_label.set_halign(Gtk.Align.START)
        self.append(self._word_label)

        self._phonetic_label = Gtk.Label()
        self._phonetic_label.add_css_class("dim-label")
        self._phonetic_label.set_valign(Gtk.Align.END)
        self.append(self._phonetic_label)

        self._audio_btn = Gtk.Button()
        self._audio_btn.set_icon_name("audio-volume-high-symbolic")
        self._audio_btn.set_tooltip_text(_("Spela uttal"))
        self._audio_btn.add_css_class("flat")
        self._audio_btn.set_valign(Gtk.Align.CENTER)
        self._audio_btn.connect("clicked", self._on_play_audio)
        self._audio_btn.set_visible(False)
        self.append(self._audio_btn)

        self._audio_url = ""
        self.set_visible(False)

    def update(self, word, phonetics):
        """Update the view with word and phonetic data."""
        if not word:
            self.set_visible(False)
            return

        self.set_visible(True)
        self._word_label.set_label(word)

        if phonetics:
            # Find first phonetic with text
            ipa_text = ""
            audio_url = ""
            for ph in phonetics:
                if ph.text and not ipa_text:
                    ipa_text = ph.text
                if ph.audio_url and not audio_url:
                    audio_url = ph.audio_url

            self._phonetic_label.set_label(ipa_text)
            self._phonetic_label.set_visible(bool(ipa_text))
            self._audio_url = audio_url
            self._audio_btn.set_visible(bool(audio_url))
        else:
            self._phonetic_label.set_visible(False)
            self._audio_btn.set_visible(False)

    def _on_play_audio(self, button):
        """Play pronunciation audio."""
        if self._audio_url:
            play_audio_url(self._audio_url)
