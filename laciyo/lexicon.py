"""
laciyo.lexicon
~~~~~~~~~~~~~~
Core vocabulary of Laciyo.

Each entry is a dict with the following keys:

    laciyo   – Laciyo orthographic form
    latin    – Classical Latin source word(s)
    pos      – part of speech  (n, v, adj, adv, prep, conj, pron, num, interj)
    gender   – 'm', 'f', 'n/a'  (nouns only; verbs/others use 'n/a')
    english  – English gloss (list of synonyms / translations)
    notes    – optional usage note (str or None)
"""

from __future__ import annotations

LEXICON: list[dict] = [
    # ------------------------------------------------------------------ nouns
    {
        "laciyo": "akwa",
        "latin": "aqua",
        "pos": "n",
        "gender": "f",
        "english": ["water"],
        "notes": None,
    },
    {
        "laciyo": "tera",
        "latin": "terra",
        "pos": "n",
        "gender": "f",
        "english": ["earth", "land", "ground"],
        "notes": None,
    },
    {
        "laciyo": "sol",
        "latin": "sol",
        "pos": "n",
        "gender": "m",
        "english": ["sun"],
        "notes": None,
    },
    {
        "laciyo": "luna",
        "latin": "luna",
        "pos": "n",
        "gender": "f",
        "english": ["moon"],
        "notes": None,
    },
    {
        "laciyo": "omo",
        "latin": "homo",
        "pos": "n",
        "gender": "m",
        "english": ["person", "human", "man"],
        "notes": "Gender-neutral in Laciyo usage.",
    },
    {
        "laciyo": "femina",
        "latin": "femina",
        "pos": "n",
        "gender": "f",
        "english": ["woman"],
        "notes": None,
    },
    {
        "laciyo": "via",
        "latin": "via",
        "pos": "n",
        "gender": "f",
        "english": ["way", "road", "path"],
        "notes": None,
    },
    {
        "laciyo": "verbu",
        "latin": "verbum",
        "pos": "n",
        "gender": "m",
        "english": ["word"],
        "notes": None,
    },
    {
        "laciyo": "tempo",
        "latin": "tempus",
        "pos": "n",
        "gender": "m",
        "english": ["time"],
        "notes": None,
    },
    {
        "laciyo": "luks",
        "latin": "lux",
        "pos": "n",
        "gender": "f",
        "english": ["light"],
        "notes": None,
    },
    {
        "laciyo": "noks",
        "latin": "nox",
        "pos": "n",
        "gender": "f",
        "english": ["night"],
        "notes": None,
    },
    {
        "laciyo": "vita",
        "latin": "vita",
        "pos": "n",
        "gender": "f",
        "english": ["life"],
        "notes": None,
    },
    {
        "laciyo": "mor",
        "latin": "mors",
        "pos": "n",
        "gender": "f",
        "english": ["death"],
        "notes": None,
    },
    {
        "laciyo": "amor",
        "latin": "amor",
        "pos": "n",
        "gender": "m",
        "english": ["love"],
        "notes": None,
    },
    {
        "laciyo": "libre",
        "latin": "liber",
        "pos": "n",
        "gender": "m",
        "english": ["book"],
        "notes": "Homograph with adj libre (free). Distinguish by context.",
    },
    {
        "laciyo": "reks",
        "latin": "rex",
        "pos": "n",
        "gender": "m",
        "english": ["king", "ruler"],
        "notes": None,
    },
    {
        "laciyo": "data",
        "latin": "data",
        "pos": "n",
        "gender": "f",
        "english": ["data", "information"],
        "notes": "Plural of 'datu' (datum); used as mass noun in Laciyo.",
    },
    {
        "laciyo": "rete",
        "latin": "rete",
        "pos": "n",
        "gender": "m",
        "english": ["network", "net", "web"],
        "notes": "Adopted as the Laciyo word for the internet.",
    },
    {
        "laciyo": "makina",
        "latin": "machina",
        "pos": "n",
        "gender": "f",
        "english": ["machine", "device"],
        "notes": None,
    },
    {
        "laciyo": "komputo",
        "latin": "computus",
        "pos": "n",
        "gender": "m",
        "english": ["computer", "calculator"],
        "notes": "Derived from computare (to calculate).",
    },
    {
        "laciyo": "skriptu",
        "latin": "scriptum",
        "pos": "n",
        "gender": "m",
        "english": ["script", "writing", "code"],
        "notes": "Used for both handwriting and software code.",
    },
    {
        "laciyo": "nodu",
        "latin": "nodus",
        "pos": "n",
        "gender": "m",
        "english": ["node", "knot", "connection point"],
        "notes": None,
    },
    {
        "laciyo": "signalu",
        "latin": "signum",
        "pos": "n",
        "gender": "m",
        "english": ["signal", "sign"],
        "notes": None,
    },
    {
        "laciyo": "ponto",
        "latin": "pons",
        "pos": "n",
        "gender": "m",
        "english": ["bridge", "port", "gateway"],
        "notes": None,
    },
    {
        "laciyo": "populo",
        "latin": "populus",
        "pos": "n",
        "gender": "m",
        "english": ["people", "population"],
        "notes": None,
    },
    {
        "laciyo": "memoria",
        "latin": "memoria",
        "pos": "n",
        "gender": "f",
        "english": ["memory", "remembrance", "storage"],
        "notes": None,
    },
    {
        "laciyo": "anima",
        "latin": "anima",
        "pos": "n",
        "gender": "f",
        "english": ["soul", "spirit", "mind"],
        "notes": None,
    },
    {
        "laciyo": "korpo",
        "latin": "corpus",
        "pos": "n",
        "gender": "m",
        "english": ["body", "corpus"],
        "notes": None,
    },
    {
        "laciyo": "lingo",
        "latin": "lingua",
        "pos": "n",
        "gender": "f",
        "english": ["language", "tongue"],
        "notes": None,
    },
    {
        "laciyo": "voz",
        "latin": "vox",
        "pos": "n",
        "gender": "f",
        "english": ["voice"],
        "notes": None,
    },
    {
        "laciyo": "kaelo",
        "latin": "caelum",
        "pos": "n",
        "gender": "m",
        "english": ["sky", "heaven", "cyberspace"],
        "notes": "Extended to mean 'cyberspace' in digital contexts.",
    },
    {
        "laciyo": "porta",
        "latin": "porta",
        "pos": "n",
        "gender": "f",
        "english": ["door", "gate", "port"],
        "notes": None,
    },
    {
        "laciyo": "muro",
        "latin": "murus",
        "pos": "n",
        "gender": "m",
        "english": ["wall", "firewall"],
        "notes": "Extended to mean 'firewall' in digital contexts.",
    },
    # ------------------------------------------------------------------ verbs
    {
        "laciyo": "ese",
        "latin": "esse",
        "pos": "v",
        "gender": "n/a",
        "english": ["be", "exist"],
        "notes": "Infinitive form. Irregular verb.",
    },
    {
        "laciyo": "dare",
        "latin": "dare",
        "pos": "v",
        "gender": "n/a",
        "english": ["give"],
        "notes": None,
    },
    {
        "laciyo": "vedere",
        "latin": "videre",
        "pos": "v",
        "gender": "n/a",
        "english": ["see", "watch"],
        "notes": None,
    },
    {
        "laciyo": "audire",
        "latin": "audire",
        "pos": "v",
        "gender": "n/a",
        "english": ["hear", "listen"],
        "notes": None,
    },
    {
        "laciyo": "dikere",
        "latin": "dicere",
        "pos": "v",
        "gender": "n/a",
        "english": ["say", "speak", "tell"],
        "notes": None,
    },
    {
        "laciyo": "fakere",
        "latin": "facere",
        "pos": "v",
        "gender": "n/a",
        "english": ["do", "make", "create"],
        "notes": None,
    },
    {
        "laciyo": "venire",
        "latin": "venire",
        "pos": "v",
        "gender": "n/a",
        "english": ["come"],
        "notes": None,
    },
    {
        "laciyo": "ire",
        "latin": "ire",
        "pos": "v",
        "gender": "n/a",
        "english": ["go"],
        "notes": None,
    },
    {
        "laciyo": "skribere",
        "latin": "scribere",
        "pos": "v",
        "gender": "n/a",
        "english": ["write", "code"],
        "notes": "Extended to mean 'write code'.",
    },
    {
        "laciyo": "legere",
        "latin": "legere",
        "pos": "v",
        "gender": "n/a",
        "english": ["read"],
        "notes": None,
    },
    {
        "laciyo": "konektere",
        "latin": "conectere",
        "pos": "v",
        "gender": "n/a",
        "english": ["connect", "link"],
        "notes": None,
    },
    {
        "laciyo": "kalkolare",
        "latin": "calculare",
        "pos": "v",
        "gender": "n/a",
        "english": ["calculate", "compute", "process"],
        "notes": None,
    },
    # --------------------------------------------------------------- adjectives
    {
        "laciyo": "grande",
        "latin": "grandis",
        "pos": "adj",
        "gender": "n/a",
        "english": ["great", "large", "big"],
        "notes": None,
    },
    {
        "laciyo": "parvo",
        "latin": "parvus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["small", "little"],
        "notes": None,
    },
    {
        "laciyo": "novo",
        "latin": "novus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["new"],
        "notes": None,
    },
    {
        "laciyo": "antiko",
        "latin": "antiquus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["old", "ancient"],
        "notes": None,
    },
    {
        "laciyo": "rapido",
        "latin": "rapidus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["fast", "rapid", "quick"],
        "notes": None,
    },
    {
        "laciyo": "lento",
        "latin": "lentus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["slow"],
        "notes": None,
    },
    {
        "laciyo": "libre",
        "latin": "liberus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["free", "open"],
        "notes": "Open-source software is 'skriptu libre'.",
    },
    {
        "laciyo": "forte",
        "latin": "fortis",
        "pos": "adj",
        "gender": "n/a",
        "english": ["strong", "powerful"],
        "notes": None,
    },
    {
        "laciyo": "verio",
        "latin": "verus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["true", "real", "genuine"],
        "notes": None,
    },
    {
        "laciyo": "falso",
        "latin": "falsus",
        "pos": "adj",
        "gender": "n/a",
        "english": ["false", "fake"],
        "notes": None,
    },
    # --------------------------------------------------------------- numbers
    {
        "laciyo": "uno",
        "latin": "unus",
        "pos": "num",
        "gender": "n/a",
        "english": ["one", "1"],
        "notes": None,
    },
    {
        "laciyo": "duo",
        "latin": "duo",
        "pos": "num",
        "gender": "n/a",
        "english": ["two", "2"],
        "notes": None,
    },
    {
        "laciyo": "tres",
        "latin": "tres",
        "pos": "num",
        "gender": "n/a",
        "english": ["three", "3"],
        "notes": None,
    },
    {
        "laciyo": "kwatro",
        "latin": "quattuor",
        "pos": "num",
        "gender": "n/a",
        "english": ["four", "4"],
        "notes": None,
    },
    {
        "laciyo": "kinke",
        "latin": "quinque",
        "pos": "num",
        "gender": "n/a",
        "english": ["five", "5"],
        "notes": None,
    },
    {
        "laciyo": "seks",
        "latin": "sex",
        "pos": "num",
        "gender": "n/a",
        "english": ["six", "6"],
        "notes": None,
    },
    {
        "laciyo": "septe",
        "latin": "septem",
        "pos": "num",
        "gender": "n/a",
        "english": ["seven", "7"],
        "notes": None,
    },
    {
        "laciyo": "okto",
        "latin": "octo",
        "pos": "num",
        "gender": "n/a",
        "english": ["eight", "8"],
        "notes": None,
    },
    {
        "laciyo": "nove",
        "latin": "novem",
        "pos": "num",
        "gender": "n/a",
        "english": ["nine", "9"],
        "notes": None,
    },
    {
        "laciyo": "deke",
        "latin": "decem",
        "pos": "num",
        "gender": "n/a",
        "english": ["ten", "10"],
        "notes": None,
    },
    # --------------------------------------------------------------- pronouns
    {
        "laciyo": "ego",
        "latin": "ego",
        "pos": "pron",
        "gender": "n/a",
        "english": ["I", "me"],
        "notes": None,
    },
    {
        "laciyo": "tu",
        "latin": "tu",
        "pos": "pron",
        "gender": "n/a",
        "english": ["you (singular)"],
        "notes": None,
    },
    {
        "laciyo": "ilo",
        "latin": "ille",
        "pos": "pron",
        "gender": "m",
        "english": ["he", "him", "it"],
        "notes": None,
    },
    {
        "laciyo": "ila",
        "latin": "illa",
        "pos": "pron",
        "gender": "f",
        "english": ["she", "her", "it"],
        "notes": None,
    },
    {
        "laciyo": "nos",
        "latin": "nos",
        "pos": "pron",
        "gender": "n/a",
        "english": ["we", "us"],
        "notes": None,
    },
    {
        "laciyo": "vos",
        "latin": "vos",
        "pos": "pron",
        "gender": "n/a",
        "english": ["you (plural)"],
        "notes": None,
    },
    {
        "laciyo": "ilos",
        "latin": "illi",
        "pos": "pron",
        "gender": "m",
        "english": ["they", "them"],
        "notes": None,
    },
    # --------------------------------------------------------------- prepositions / conjunctions
    {
        "laciyo": "ad",
        "latin": "ad",
        "pos": "prep",
        "gender": "n/a",
        "english": ["to", "toward", "at"],
        "notes": None,
    },
    {
        "laciyo": "de",
        "latin": "de",
        "pos": "prep",
        "gender": "n/a",
        "english": ["of", "from", "about"],
        "notes": None,
    },
    {
        "laciyo": "in",
        "latin": "in",
        "pos": "prep",
        "gender": "n/a",
        "english": ["in", "into", "on"],
        "notes": None,
    },
    {
        "laciyo": "et",
        "latin": "et",
        "pos": "conj",
        "gender": "n/a",
        "english": ["and"],
        "notes": None,
    },
    {
        "laciyo": "sed",
        "latin": "sed",
        "pos": "conj",
        "gender": "n/a",
        "english": ["but"],
        "notes": None,
    },
    {
        "laciyo": "si",
        "latin": "si",
        "pos": "conj",
        "gender": "n/a",
        "english": ["if"],
        "notes": None,
    },
    {
        "laciyo": "non",
        "latin": "non",
        "pos": "adv",
        "gender": "n/a",
        "english": ["not", "no"],
        "notes": None,
    },
    {
        "laciyo": "sike",
        "latin": "sic",
        "pos": "adv",
        "gender": "n/a",
        "english": ["yes", "thus", "so"],
        "notes": None,
    },
]

# Build fast lookup indices
_BY_LACIYO: dict[str, dict] = {e["laciyo"]: e for e in LEXICON}
_BY_LATIN: dict[str, dict] = {e["latin"]: e for e in LEXICON}
_BY_ENGLISH: dict[str, list[dict]] = {}
for _entry in LEXICON:
    for _gloss in _entry["english"]:
        _BY_ENGLISH.setdefault(_gloss.lower(), []).append(_entry)


def lookup(
    word: str,
    source: str = "english",
) -> list[dict] | dict | None:
    """
    Look up a word in the Laciyo lexicon.

    Parameters
    ----------
    word:
        The word to look up.
    source:
        One of ``'english'``, ``'laciyo'``, or ``'latin'``.

    Returns
    -------
    For ``source='english'``: a list of matching entries (may be empty).
    For ``source='laciyo'`` or ``source='latin'``: a single entry or ``None``.

    Examples
    --------
    >>> lookup("water")
    [{'laciyo': 'akwa', 'latin': 'aqua', ...}]
    >>> lookup("akwa", source="laciyo")
    {'laciyo': 'akwa', 'latin': 'aqua', ...}
    """
    if source == "english":
        return _BY_ENGLISH.get(word.lower(), [])
    if source == "laciyo":
        return _BY_LACIYO.get(word.lower())
    if source == "latin":
        return _BY_LATIN.get(word)
    raise ValueError(f"Unknown source '{source}'. Use 'english', 'laciyo', or 'latin'.")
