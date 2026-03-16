"""Free Dictionary API provider."""

import json
import urllib.request
import urllib.error

from lexiscan.lookup.base import LookupProvider
from lexiscan.models.result import LookupResult, Definition, Phonetic


class FreeDictProvider(LookupProvider):
    """Looks up words using the Free Dictionary API."""

    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries"

    def lookup(self, word: str, source_lang: str = "sv", target_lang: str = "en") -> LookupResult:
        result = LookupResult(word=word)

        # Try Swedish first, then English
        for lang in [source_lang, target_lang]:
            try:
                url = f"{self.BASE_URL}/{lang}/{urllib.request.quote(word)}"
                req = urllib.request.Request(url, headers={"User-Agent": "LexiScan/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())

                if isinstance(data, list) and data:
                    self._parse_response(data[0], result, lang)
                    break
            except (urllib.error.URLError, json.JSONDecodeError, KeyError):
                continue

        return result

    def _parse_response(self, entry: dict, result: LookupResult, lang: str):
        """Parse a Free Dictionary API response entry."""
        # Phonetics
        for ph in entry.get("phonetics", []):
            phonetic = Phonetic(
                text=ph.get("text", ""),
                audio_url=ph.get("audio", ""),
            )
            if phonetic.text or phonetic.audio_url:
                result.phonetics.append(phonetic)

        # Meanings
        for meaning in entry.get("meanings", []):
            pos = meaning.get("partOfSpeech", "")
            for defn in meaning.get("definitions", []):
                definition = Definition(
                    word=result.word,
                    part_of_speech=pos,
                    meaning=defn.get("definition", ""),
                    example=defn.get("example", ""),
                    synonyms=defn.get("synonyms", [])[:5],
                    language=lang,
                )
                result.definitions.append(definition)
