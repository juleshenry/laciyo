"""
laciyo.phonology
~~~~~~~~~~~~~~~~
Phonological transformation rules that convert Classical Latin orthography
into Laciyo orthography (and back).

Laciyo phonological rules (applied in order)
---------------------------------------------
1.  Long-vowel macrons removed (ā→a, ē→e, ī→i, ō→o, ū→u).
2.  'ph' → 'f'   (Greek loanwords: philosophia → filosofia)
3.  'th' → 't'   (theoria → teoria)
4.  'qu' → 'kw'  (aqua → akwa)
5.  'x'  → 'ks'  (rex → reks)
6.  'y'  → 'i'   (gymnasium → gimnasiu)
7.  'c'  before e/i/ae/oe → 's'  (caelum → selum)  [late-Latin tendency]
8.  'c'  elsewhere → 'k'          (caro → karo)
9.  'ti' before a vowel → 'si'   (gratia → grasia)
10. Final '-us' → '-o'            (dominus → domino)
11. Final '-um' → '-u'            (verbum → verbu)
12. Final '-ae' → '-e'            (aquae → ake)
13. Final '-am' / '-em' → '-a'/'-e'  (drop nasal)
14. Final '-m'  → dropped         (aquam → akwa)
15. Double consonants → single    (terra → tera … except rr which stays)
"""

import re
import unicodedata

# ---------------------------------------------------------------------------
# Macron → plain vowel map
# ---------------------------------------------------------------------------
_MACRON_MAP: dict[str, str] = {
    "ā": "a", "Ā": "A",
    "ē": "e", "Ē": "E",
    "ī": "i", "Ī": "I",
    "ō": "o", "Ō": "O",
    "ū": "u", "Ū": "U",
}

# ---------------------------------------------------------------------------
# Ordered substitution rules  (pattern, replacement)
# ---------------------------------------------------------------------------
_RULES: list[tuple[str, str]] = [
    # Greek-derived clusters
    (r"ph", "f"),
    (r"th", "t"),
    # qu → kw
    (r"qu", "kw"),
    # x → ks
    (r"x", "ks"),
    # y → i
    (r"y", "i"),
    # c before the ae/oe diphthongs → s (handles caelum, coepit, etc.)
    (r"cae", "se"),
    (r"coe", "se"),
    # c before front vowels e/i → s
    (r"c(?=[eiéí])", "s"),
    # remaining c → k
    (r"c", "k"),
    # ti before vowel → si
    (r"ti(?=[aeiouáéíóú])", "si"),
    # ---- terminal morphology ----
    # -us  → -o
    (r"us\b", "o"),
    # -um  → -u
    (r"um\b", "u"),
    # -ae  → -e
    (r"ae\b", "e"),
    # -am / -em  (accusative singular endings) drop nasal
    (r"am\b", "a"),
    (r"em\b", "e"),
    # remaining final -m
    (r"m\b", ""),
    # double consonants → single (skip rr intentionally kept as rr)
    (r"([bcdfghjklmnpqstvwz])\1", r"\1"),
]

# Compile for speed
_COMPILED: list[tuple[re.Pattern, str]] = [
    (re.compile(pat, re.IGNORECASE), repl) for pat, repl in _RULES
]


def _strip_macrons(text: str) -> str:
    """Replace Unicode macron-vowels with plain ASCII equivalents."""
    result = []
    for ch in text:
        result.append(_MACRON_MAP.get(ch, ch))
    return "".join(result)


def latinise(latin_word: str) -> str:
    """
    Convert a Classical Latin orthographic form into its Laciyo equivalent.

    Parameters
    ----------
    latin_word:
        A word (or short phrase) in Classical Latin spelling.

    Returns
    -------
    str
        The Laciyo form.

    Examples
    --------
    >>> latinise("aqua")
    'akwa'
    >>> latinise("verbum")
    'verbu'
    >>> latinise("philosophia")
    'filosofia'
    >>> latinise("rex")
    'reks'
    """
    word = _strip_macrons(latin_word)
    for pattern, replacement in _COMPILED:
        word = pattern.sub(replacement, word)
    return word


def romanise(laciyo_word: str) -> str:
    """
    Approximate reverse mapping: Laciyo orthography → a Romanised form.

    This is a *best-effort* heuristic; Latin is not fully recoverable from
    Laciyo because the transformation is lossy.

    Parameters
    ----------
    laciyo_word:
        A word in Laciyo orthography.

    Returns
    -------
    str
        An approximate Classical Latin spelling.

    Examples
    --------
    >>> romanise("akwa")
    'aqua'
    >>> romanise("verbu")
    'verbum'
    """
    word = laciyo_word
    # kw → qu
    word = re.sub(r"kw", "qu", word, flags=re.IGNORECASE)
    # ks → x
    word = re.sub(r"ks", "x", word, flags=re.IGNORECASE)
    # f → ph  (only if followed by a vowel, crude heuristic)
    word = re.sub(r"f(?=[aeiou])", "ph", word, flags=re.IGNORECASE)
    # s → c  before e/i  (heuristic reversal)
    word = re.sub(r"s(?=[ei])", "c", word, flags=re.IGNORECASE)
    # si before vowel → ti
    word = re.sub(r"si(?=[aeiou])", "ti", word, flags=re.IGNORECASE)
    # final -o → -us
    word = re.sub(r"o\b", "us", word, flags=re.IGNORECASE)
    # final -u → -um
    word = re.sub(r"u\b", "um", word, flags=re.IGNORECASE)
    # k → c
    word = re.sub(r"k", "c", word, flags=re.IGNORECASE)
    return word
