"""Aggregates results from multiple lookup providers."""

import threading
from concurrent.futures import ThreadPoolExecutor

from lexiscan.models.result import LookupResult
from lexiscan.lookup.freedict import FreeDictProvider
from lexiscan.lookup.lexin import LexinProvider
from lexiscan.lookup.arasaac import ArasaacProvider


class LookupAggregator:
    """Fans out lookups to all providers and merges results."""

    def __init__(self):
        self._providers = [
            FreeDictProvider(),
            LexinProvider(),
            ArasaacProvider(),
        ]
        self._executor = ThreadPoolExecutor(max_workers=3)

    def lookup(self, word: str, callback=None, source_lang: str = "sv", target_lang: str = "en"):
        """Look up a word across all providers. Calls callback with merged result."""
        thread = threading.Thread(
            target=self._do_lookup,
            args=(word, callback, source_lang, target_lang),
            daemon=True,
        )
        thread.start()

    def _do_lookup(self, word, callback, source_lang, target_lang):
        """Perform lookup in background thread."""
        merged = LookupResult(word=word)

        futures = []
        for provider in self._providers:
            future = self._executor.submit(
                provider.lookup, word, source_lang, target_lang
            )
            futures.append(future)

        for future in futures:
            try:
                result = future.result(timeout=10)
                self._merge(merged, result)
            except Exception:
                continue

        if callback:
            callback(merged)

    def _merge(self, target: LookupResult, source: LookupResult):
        """Merge source results into target."""
        target.definitions.extend(source.definitions)
        target.phonetics.extend(source.phonetics)
        target.translations.extend(source.translations)
        target.images.extend(source.images)
