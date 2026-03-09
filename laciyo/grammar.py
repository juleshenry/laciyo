"""
laciyo.grammar
~~~~~~~~~~~~~~
Grammar rules for Laciyo – Latin Cyber Creole.

Overview
--------
Laciyo simplifies Classical Latin grammar while retaining its essential
character.  Key features:

**Nouns**
- Two genders: masculine (m) and feminine (f).
- Two numbers: singular and plural.
- Plural formation:
    * Most masculine nouns (ending in -o): -o → -os  (domino → dominos)
    * Most feminine nouns (ending -a):    -a → -ae   (luna → lunae)
    * Nouns ending in a consonant:          + -es      (sol → soles)
    * Irregular forms stored in PLURAL_IRREGULARS.

**Verbs**
- Infinitive ends in -re (ese, dare, vedere, …).
- Present tense conjugation (regular):

    Person  | Singular | Plural
    --------|----------|--------
    1st     | -o       | -amos
    2nd     | -as      | -atis
    3rd     | -at      | -ant

- The stem is the infinitive minus -re, then adjusted:
    * Stems ending in -e (vedere → vede-) drop the -e before adding endings.
    * Stems ending in a consonant take endings directly.
- Irregular verb: ese (to be) – see IRREGULAR_CONJUGATIONS.

**Adjectives**
- Invariable for gender in Laciyo (simplification).
- Plural: add -s if ending in a vowel, -es if ending in a consonant.

**Word order**
- Default SVO (Subject – Verb – Object).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Irregular plural nouns
# ---------------------------------------------------------------------------
PLURAL_IRREGULARS: dict[str, str] = {
    "omo": "omines",       # homo → homines
    "mor": "mores",        # mors → mores
    "lingo": "lingwes",    # lingua → linguae → lingwes
    "voz": "vozes",
    "reks": "reges",       # rex → reges
    "luks": "luces",       # lux → luces
    "noks": "noktes",      # nox → noctes
    "ponto": "pontes",     # pons → pontes
    "komputo": "komputos",
}

# ---------------------------------------------------------------------------
# Irregular verb conjugations
# ---------------------------------------------------------------------------
# Structure: {infinitive: {person_number: form}}
# person_number keys: "1sg", "2sg", "3sg", "1pl", "2pl", "3pl"
IRREGULAR_CONJUGATIONS: dict[str, dict[str, str]] = {
    "ese": {
        "1sg": "so",
        "2sg": "es",
        "3sg": "est",
        "1pl": "samos",
        "2pl": "estis",
        "3pl": "sont",
    },
    "ire": {
        "1sg": "eo",
        "2sg": "is",
        "3sg": "it",
        "1pl": "iamos",
        "2pl": "itis",
        "3pl": "eont",
    },
}

# ---------------------------------------------------------------------------
# Person/number labels
# ---------------------------------------------------------------------------
PERSONS = ("1sg", "2sg", "3sg", "1pl", "2pl", "3pl")
_ENDINGS = {
    "1sg": "o",
    "2sg": "as",
    "3sg": "at",
    "1pl": "amos",
    "2pl": "atis",
    "3pl": "ant",
}


def _get_stem(infinitive: str) -> str:
    """
    Derive the present-tense stem from a Laciyo infinitive.

    Rules
    -----
    * Strip trailing -re.
    * If the resulting stem ends in -e, drop it (vedere → ved-).
    * Otherwise keep as-is (audire → audi-).
    """
    if not infinitive.endswith("re"):
        raise ValueError(
            f"'{infinitive}' does not look like a Laciyo infinitive (should end in -re)."
        )
    stem = infinitive[:-2]  # drop -re
    if stem.endswith("e"):
        stem = stem[:-1]    # drop trailing -e
    return stem


def conjugate(infinitive: str, person: str = "3sg") -> str:
    """
    Conjugate a Laciyo verb in the present tense.

    Parameters
    ----------
    infinitive:
        The Laciyo infinitive form (ending in -re).
    person:
        One of '1sg', '2sg', '3sg', '1pl', '2pl', '3pl'.

    Returns
    -------
    str
        Conjugated present-tense form.

    Raises
    ------
    ValueError
        If *person* is not recognised or *infinitive* is malformed.

    Examples
    --------
    >>> conjugate("vedere", "1sg")
    'vedo'
    >>> conjugate("audire", "3pl")
    'audant'
    >>> conjugate("ese", "1sg")
    'so'
    """
    if person not in PERSONS:
        raise ValueError(
            f"Unknown person '{person}'. Choose from: {', '.join(PERSONS)}"
        )
    # Irregular?
    if infinitive in IRREGULAR_CONJUGATIONS:
        return IRREGULAR_CONJUGATIONS[infinitive][person]
    # Regular
    stem = _get_stem(infinitive)
    ending = _ENDINGS[person]
    # Avoid double vowel: stem ends in vowel + ending starts with vowel
    stem_ends_vowel = stem and stem[-1] in "aeiou"
    ending_starts_vowel = ending and ending[0] in "aeiou"
    if stem_ends_vowel and ending_starts_vowel:
        # drop stem final vowel before vowel-initial ending (sandhi rule)
        stem = stem[:-1]
    return stem + ending


def pluralise(noun: str, gender: str = "m") -> str:
    """
    Return the plural form of a Laciyo noun.

    Parameters
    ----------
    noun:
        The singular Laciyo noun.
    gender:
        ``'m'`` (masculine) or ``'f'`` (feminine).

    Returns
    -------
    str
        Plural form.

    Examples
    --------
    >>> pluralise("luna", "f")
    'lunae'
    >>> pluralise("komputo", "m")
    'komputos'
    >>> pluralise("sol", "m")
    'soles'
    """
    if noun in PLURAL_IRREGULARS:
        return PLURAL_IRREGULARS[noun]
    if noun.endswith("a") and gender == "f":
        return noun[:-1] + "ae"
    if noun.endswith("o") and gender == "m":
        return noun + "s"
    # ends in consonant (or -i, -e, -u)
    if noun[-1] in "bcdfghjklmnprstvwz":
        return noun + "es"
    # default: add -s
    return noun + "s"


def full_conjugation(infinitive: str) -> dict[str, str]:
    """
    Return the full present-tense paradigm for a verb.

    Parameters
    ----------
    infinitive:
        Laciyo infinitive.

    Returns
    -------
    dict mapping person keys to conjugated forms.

    Examples
    --------
    >>> full_conjugation("ese")
    {'1sg': 'so', '2sg': 'es', '3sg': 'est', '1pl': 'samos', '2pl': 'estis', '3pl': 'sont'}
    """
    return {p: conjugate(infinitive, p) for p in PERSONS}
