"""Localization module for multi-language support"""

from .vi import TRANSLATIONS as VI_TRANSLATIONS
from .en import TRANSLATIONS as EN_TRANSLATIONS

LANGUAGES = {
    "vi": {"name": "Tiếng Việt", "flag": "🇻🇳", "translations": VI_TRANSLATIONS},
    "en": {"name": "English", "flag": "🇺🇸", "translations": EN_TRANSLATIONS}
}
