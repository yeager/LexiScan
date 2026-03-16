"""Data models for lookup results."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Definition:
    word: str
    part_of_speech: str = ""
    meaning: str = ""
    example: str = ""
    synonyms: List[str] = field(default_factory=list)
    language: str = "sv"


@dataclass
class Phonetic:
    text: str = ""
    audio_url: str = ""


@dataclass
class Translation:
    source_word: str = ""
    source_lang: str = "sv"
    target_word: str = ""
    target_lang: str = "en"
    part_of_speech: str = ""


@dataclass
class ImageResult:
    image_url: str = ""
    description: str = ""
    provider: str = "arasaac"


@dataclass
class LookupResult:
    word: str = ""
    definitions: List[Definition] = field(default_factory=list)
    phonetics: List[Phonetic] = field(default_factory=list)
    translations: List[Translation] = field(default_factory=list)
    images: List[ImageResult] = field(default_factory=list)

    def is_empty(self) -> bool:
        return (
            not self.definitions
            and not self.translations
            and not self.images
        )
