"""Internationalization support using gettext."""

import gettext
import locale
import os

_translations = None


def setup_i18n():
    """Initialize gettext for the application."""
    global _translations

    localedir = os.path.join(os.path.dirname(__file__), "..", "..", "po", "locale")
    if not os.path.isdir(localedir):
        localedir = os.path.join("/usr", "share", "locale")

    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        pass

    try:
        _translations = gettext.translation(
            "lexiscan", localedir=localedir, fallback=True
        )
        _translations.install()
    except Exception:
        _translations = gettext.NullTranslations()
        _translations.install()


def _(message):
    """Translate a message string."""
    global _translations
    if _translations is None:
        return message
    return _translations.gettext(message)


def ngettext(singular, plural, n):
    """Translate a message with plural form."""
    global _translations
    if _translations is None:
        return singular if n == 1 else plural
    return _translations.ngettext(singular, plural, n)
