"""Free Google Translate API for Python. Translates totally free of charge."""
__all__ = 'Translator',
__version__ = '3.1.0-alpha'

import httpcore
from Toolkit.Translation.googletrans.client import Translator
from Toolkit.Translation.googletrans.constants import LANGCODES, LANGUAGES  # noqa
