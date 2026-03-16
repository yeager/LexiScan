"""Abstract base class for lookup providers."""

from abc import ABC, abstractmethod
from lexiscan.models.result import LookupResult


class LookupProvider(ABC):
    """Base class for dictionary/image lookup providers."""

    @abstractmethod
    def lookup(self, word: str, source_lang: str = "sv", target_lang: str = "en") -> LookupResult:
        """Look up a word and return results."""
        ...
