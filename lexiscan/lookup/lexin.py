"""Swedish-English translation provider using Lexin/Folkets Lexikon."""

import json
import urllib.request
import urllib.error

from lexiscan.lookup.base import LookupProvider
from lexiscan.models.result import LookupResult, Translation, Definition


class LexinProvider(LookupProvider):
    """Swedish-English translation via Folkets Lexikon / free translation APIs."""

    # Folkets Lexikon API endpoint (community mirror)
    FOLKETS_URL = "https://folkets-lexikon.csc.kth.se/folkets/service"

    def lookup(self, word: str, source_lang: str = "sv", target_lang: str = "en") -> LookupResult:
        result = LookupResult(word=word)

        # Try Folkets Lexikon
        try:
            self._lookup_folkets(word, result, source_lang, target_lang)
        except Exception:
            pass

        # Fallback: MyMemory translation API (free, no key needed)
        if not result.translations:
            try:
                self._lookup_mymemory(word, result, source_lang, target_lang)
            except Exception:
                pass

        return result

    def _lookup_folkets(self, word: str, result: LookupResult, src: str, tgt: str):
        """Query Folkets Lexikon for Swedish-English translations."""
        url = f"{self.FOLKETS_URL}?lang=sv&interface=en&word={urllib.request.quote(word)}"
        req = urllib.request.Request(url, headers={"User-Agent": "LexiScan/1.0"})

        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                content = resp.read().decode("utf-8")

            # Parse the simple text/XML response
            if "translation" in content.lower() or "definition" in content.lower():
                # Basic parsing of Folkets response
                for line in content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("<") and not line.startswith("<?"):
                        translation = Translation(
                            source_word=word,
                            source_lang=src,
                            target_word=line,
                            target_lang=tgt,
                        )
                        result.translations.append(translation)
                        if len(result.translations) >= 5:
                            break
        except (urllib.error.URLError, UnicodeDecodeError):
            pass

    def _lookup_mymemory(self, word: str, result: LookupResult, src: str, tgt: str):
        """Fallback translation via MyMemory API."""
        langpair = f"{src}|{tgt}"
        url = (
            f"https://api.mymemory.translated.net/get?"
            f"q={urllib.request.quote(word)}&langpair={langpair}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "LexiScan/1.0"})

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())

        if data.get("responseStatus") == 200:
            translated = data.get("responseData", {}).get("translatedText", "")
            if translated and translated.lower() != word.lower():
                result.translations.append(Translation(
                    source_word=word,
                    source_lang=src,
                    target_word=translated,
                    target_lang=tgt,
                ))

            # Additional matches
            for match in data.get("matches", [])[:4]:
                segment = match.get("segment", "")
                translation_text = match.get("translation", "")
                if (translation_text and translation_text.lower() != word.lower()
                        and translation_text != translated):
                    result.translations.append(Translation(
                        source_word=segment or word,
                        source_lang=src,
                        target_word=translation_text,
                        target_lang=tgt,
                    ))
