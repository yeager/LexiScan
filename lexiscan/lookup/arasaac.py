"""ARASAAC pictogram provider."""

import json
import urllib.request
import urllib.error

from lexiscan.lookup.base import LookupProvider
from lexiscan.models.result import LookupResult, ImageResult


class ArasaacProvider(LookupProvider):
    """Looks up pictograms from ARASAAC API."""

    BASE_URL = "https://api.arasaac.org/v1"

    def lookup(self, word: str, source_lang: str = "sv", target_lang: str = "en") -> LookupResult:
        result = LookupResult(word=word)

        # Try Swedish first, then English
        for lang in [source_lang, target_lang]:
            locale = self._lang_to_locale(lang)
            try:
                images = self._search_pictograms(word, locale)
                result.images.extend(images)
                if result.images:
                    break
            except Exception:
                continue

        return result

    def _search_pictograms(self, word: str, locale: str) -> list:
        """Search ARASAAC for pictograms matching a word."""
        url = f"{self.BASE_URL}/pictograms/{locale}/search/{urllib.request.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": "LexiScan/1.0"})

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        images = []
        if isinstance(data, list):
            for item in data[:3]:  # Limit to 3 pictograms
                picto_id = item.get("_id", "")
                if picto_id:
                    image_url = f"{self.BASE_URL}/pictograms/{picto_id}?download=false"
                    keywords = item.get("keywords", [])
                    desc = keywords[0].get("keyword", word) if keywords else word
                    images.append(ImageResult(
                        image_url=image_url,
                        description=desc,
                        provider="arasaac",
                    ))

        return images

    def _lang_to_locale(self, lang: str) -> str:
        """Convert language code to ARASAAC locale."""
        mapping = {
            "sv": "sv",
            "en": "en",
            "es": "es",
            "fr": "fr",
            "de": "de",
        }
        return mapping.get(lang, "en")
