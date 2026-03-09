"""
Laciyo – Latin Cyber Creole
A constructed language (conlang) that reconstitutes Classical Latin into a
simplified, modern, cyberpunk-flavoured creole.

Core design principles
----------------------
1. Vocabulary drawn directly from Latin roots.
2. Phonology regularised and simplified (no long-vowel distinction, consonant
   cluster simplification, etc.).
3. Grammar stripped to two genders, two number forms, and a simplified verbal
   paradigm – making Laciyo learnable while remaining unmistakably Latin.
4. Open to neologisms for digital / technical concepts, all coined from Latin
   or Greek roots that entered Latin.
"""

__version__ = "0.1.0"
__author__ = "Laciyo Project"

from laciyo.phonology import latinise, romanise   # noqa: F401
from laciyo.lexicon import LEXICON, lookup         # noqa: F401
from laciyo.grammar import conjugate, pluralise    # noqa: F401
from laciyo.translator import Translator           # noqa: F401
