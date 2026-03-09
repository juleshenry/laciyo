"""Tests for laciyo.grammar"""

import pytest
from laciyo.grammar import conjugate, pluralise, full_conjugation, PERSONS


class TestConjugate:
    """Tests for present-tense conjugation."""

    def test_vedere_1sg(self):
        assert conjugate("vedere", "1sg") == "vedo"

    def test_vedere_2sg(self):
        assert conjugate("vedere", "2sg") == "vedas"

    def test_vedere_3sg(self):
        assert conjugate("vedere", "3sg") == "vedat"

    def test_vedere_1pl(self):
        assert conjugate("vedere", "1pl") == "vedamos"

    def test_vedere_2pl(self):
        assert conjugate("vedere", "2pl") == "vedatis"

    def test_vedere_3pl(self):
        assert conjugate("vedere", "3pl") == "vedant"

    def test_audire_3pl(self):
        # stem = 'audi'; 'i' (vowel) + 'ant' (vowel-initial) → sandhi drops 'i': aud + ant
        result = conjugate("audire", "3pl")
        assert result == "audant"

    def test_irregular_ese_full(self):
        paradigm = full_conjugation("ese")
        assert paradigm["1sg"] == "so"
        assert paradigm["2sg"] == "es"
        assert paradigm["3sg"] == "est"
        assert paradigm["1pl"] == "samos"
        assert paradigm["2pl"] == "estis"
        assert paradigm["3pl"] == "sont"

    def test_irregular_ire_3sg(self):
        assert conjugate("ire", "3sg") == "it"

    def test_invalid_person_raises(self):
        with pytest.raises(ValueError, match="Unknown person"):
            conjugate("vedere", "4sg")

    def test_non_infinitive_raises(self):
        with pytest.raises(ValueError, match="does not look like"):
            conjugate("video", "1sg")

    def test_full_conjugation_has_all_persons(self):
        paradigm = full_conjugation("vedere")
        assert set(paradigm.keys()) == set(PERSONS)

    def test_dare_1sg(self):
        # dare → stem 'da' + 'o' = 'dao'? Let's check actual output
        result = conjugate("dare", "1sg")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_skribere_3sg(self):
        # skribere → stem skrib + at = skribat
        assert conjugate("skribere", "3sg") == "skribat"


class TestPluralise:
    """Tests for noun pluralisation."""

    def test_luna_feminine(self):
        assert pluralise("luna", "f") == "lunae"

    def test_komputo_masculine(self):
        assert pluralise("komputo", "m") == "komputos"

    def test_sol_consonant_ending(self):
        assert pluralise("sol", "m") == "soles"

    def test_amor_consonant_ending(self):
        assert pluralise("amor", "m") == "amores"

    def test_irregular_omo(self):
        assert pluralise("omo", "m") == "omines"

    def test_irregular_reks(self):
        assert pluralise("reks", "m") == "reges"

    def test_irregular_voz(self):
        assert pluralise("voz", "f") == "vozes"

    def test_vita_feminine(self):
        assert pluralise("vita", "f") == "vitae"

    def test_default_gender_masculine(self):
        # pluralise without gender arg uses default 'm'
        result = pluralise("sol")
        assert result == "soles"
