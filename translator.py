import json
from functools import lru_cache
from pathlib import Path

import streamlit as st

LANG_FILES = {
    "en": "i18n/en.json",
    "es": "i18n/es.json",
}


@lru_cache(maxsize=None)
def _load_translations(language: str) -> dict[str, str]:
    """Load translation mapping for given language and cache it."""
    filename = LANG_FILES.get(language, LANG_FILES["en"])
    file_path = Path(__file__).resolve().parent / filename
    with file_path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def translate(key: str, **kwargs) -> str:
    """Return translation for key based on current session language."""
    language = getattr(st.session_state, "language", "en")
    translations = _load_translations(language)
    text = translations.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text
