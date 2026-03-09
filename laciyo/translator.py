"""
laciyo.translator
~~~~~~~~~~~~~~~~~
High-level translation interface for Laciyo.

The :class:`Translator` class provides:

* ``latin_to_laciyo(text)``  – phonological + morphological adaptation of a
  Classical Latin text into Laciyo.
* ``english_to_laciyo(word)`` – look up a single English word in the lexicon
  and return the Laciyo equivalent(s).
* ``laciyo_to_english(word)`` – reverse lookup from Laciyo to English gloss.
* ``phrase(subject, verb_inf, obj)`` – construct a basic SVO sentence.
"""

from __future__ import annotations

from laciyo.phonology import latinise
from laciyo.lexicon import lookup, LEXICON
from laciyo.grammar import conjugate, pluralise


class Translator:
    """
    Laciyo translation helper.

    Examples
    --------
    >>> t = Translator()
    >>> t.latin_to_laciyo("aqua vita est")
    'akwa vita est'
    >>> t.english_to_laciyo("water")
    ['akwa']
    >>> t.laciyo_to_english("akwa")
    ['water']
    """

    # ------------------------------------------------------------------
    def latin_to_laciyo(self, text: str) -> str:
        """
        Convert a Latin text (space-separated words) into Laciyo.

        Each word is first checked against the lexicon (exact Latin match).
        If found, the canonical Laciyo form is returned.  Otherwise the
        phonological rules are applied automatically.

        Parameters
        ----------
        text:
            A Latin word or phrase.

        Returns
        -------
        str
            The Laciyo rendering.
        """
        words = text.split()
        result = []
        for word in words:
            # Strip trailing punctuation for lookup
            punct = ""
            if word and word[-1] in ".,;:!?":
                punct = word[-1]
                word = word[:-1]

            entry = lookup(word, source="latin")
            if entry:
                result.append(entry["laciyo"] + punct)
            else:
                result.append(latinise(word) + punct)
        return " ".join(result)

    # ------------------------------------------------------------------
    def english_to_laciyo(self, word: str) -> list[str]:
        """
        Translate an English word to its Laciyo equivalent(s).

        Parameters
        ----------
        word:
            English word to translate.

        Returns
        -------
        list[str]
            Laciyo words that match, or an empty list if none found.
        """
        entries = lookup(word, source="english")
        return [e["laciyo"] for e in entries]

    # ------------------------------------------------------------------
    def laciyo_to_english(self, word: str) -> list[str]:
        """
        Translate a Laciyo word to its English gloss(es).

        Parameters
        ----------
        word:
            Laciyo word.

        Returns
        -------
        list[str]
            English meanings, or an empty list if not found.
        """
        entry = lookup(word, source="laciyo")
        if entry:
            return list(entry["english"])
        return []

    # ------------------------------------------------------------------
    def phrase(
        self,
        subject: str,
        verb_infinitive: str,
        obj: str | None = None,
        person: str = "3sg",
    ) -> str:
        """
        Build a simple Laciyo SVO sentence.

        Parameters
        ----------
        subject:
            Laciyo noun or pronoun (nominative).
        verb_infinitive:
            Laciyo verb infinitive (ending in -re).
        obj:
            Optional Laciyo object noun.
        person:
            Verb person/number ('1sg', '2sg', '3sg', '1pl', '2pl', '3pl').

        Returns
        -------
        str
            Formatted sentence with a trailing full-stop.

        Examples
        --------
        >>> t = Translator()
        >>> t.phrase("ego", "vedere", "luna")
        'ego vedo luna.'
        >>> t.phrase("akwa", "ese", person="3sg")
        'akwa est.'
        """
        verb_form = conjugate(verb_infinitive, person)
        parts = [subject, verb_form]
        if obj:
            parts.append(obj)
        return " ".join(parts) + "."

    # ------------------------------------------------------------------
    def dictionary(self, pos_filter: str | None = None) -> list[dict]:
        """
        Return the full Laciyo lexicon, optionally filtered by part of speech.

        Parameters
        ----------
        pos_filter:
            Part of speech abbreviation (e.g. ``'n'``, ``'v'``, ``'adj'``).
            If ``None``, all entries are returned.

        Returns
        -------
        list[dict]
            Lexicon entries.
        """
        if pos_filter is None:
            return list(LEXICON)
        return [e for e in LEXICON if e["pos"] == pos_filter]
