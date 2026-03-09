"""Tests for laciyo.translator"""

import pytest
from laciyo.translator import Translator


@pytest.fixture
def t():
    return Translator()


class TestLatinToLaciyo:
    def test_single_word_in_lexicon(self, t):
        # 'aqua' is in lexicon, should return canonical form
        assert t.latin_to_laciyo("aqua") == "akwa"

    def test_single_word_phonology_fallback(self, t):
        # 'philosophus' is not in lexicon; phonology rules apply
        result = t.latin_to_laciyo("philosophus")
        assert result == "filosofo"

    def test_phrase_mixed(self, t):
        result = t.latin_to_laciyo("aqua vita est")
        assert result == "akwa vita est"

    def test_punctuation_preserved(self, t):
        result = t.latin_to_laciyo("aqua.")
        assert result == "akwa."

    def test_phrase_verbum(self, t):
        result = t.latin_to_laciyo("verbum")
        assert result == "verbu"


class TestEnglishToLaciyo:
    def test_water(self, t):
        assert "akwa" in t.english_to_laciyo("water")

    def test_life(self, t):
        assert "vita" in t.english_to_laciyo("life")

    def test_not_found(self, t):
        assert t.english_to_laciyo("xyzzy") == []

    def test_network(self, t):
        result = t.english_to_laciyo("network")
        assert "rete" in result


class TestLaciyoToEnglish:
    def test_akwa(self, t):
        assert "water" in t.laciyo_to_english("akwa")

    def test_vita(self, t):
        assert "life" in t.laciyo_to_english("vita")

    def test_not_found(self, t):
        assert t.laciyo_to_english("xyzzy") == []

    def test_rete(self, t):
        meanings = t.laciyo_to_english("rete")
        assert "network" in meanings or "net" in meanings


class TestPhrase:
    def test_basic_intransitive(self, t):
        result = t.phrase("akwa", "ese", person="3sg")
        assert result == "akwa est."

    def test_transitive(self, t):
        result = t.phrase("ego", "vedere", "luna", person="1sg")
        assert result == "ego vedo luna."
    def test_phrase_ends_with_period(self, t):
        result = t.phrase("sol", "ese")
        assert result.endswith(".")


class TestDictionary:
    def test_returns_list(self, t):
        assert isinstance(t.dictionary(), list)

    def test_all_entries_returned_without_filter(self, t):
        from laciyo.lexicon import LEXICON
        assert len(t.dictionary()) == len(LEXICON)

    def test_pos_filter_nouns(self, t):
        nouns = t.dictionary(pos_filter="n")
        assert all(e["pos"] == "n" for e in nouns)
        assert len(nouns) > 0

    def test_pos_filter_verbs(self, t):
        verbs = t.dictionary(pos_filter="v")
        assert all(e["pos"] == "v" for e in verbs)
        assert len(verbs) > 0

    def test_pos_filter_empty(self, t):
        # No entries for a nonsense POS
        assert t.dictionary(pos_filter="xyz") == []
