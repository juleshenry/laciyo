"""Tests for laciyo.lexicon"""

import pytest
from laciyo.lexicon import LEXICON, lookup


class TestLexiconStructure:
    """Verify structural integrity of every lexicon entry."""

    REQUIRED_KEYS = {"laciyo", "latin", "pos", "gender", "english", "notes"}
    VALID_POS = {"n", "v", "adj", "adv", "prep", "conj", "pron", "num", "interj"}
    VALID_GENDER = {"m", "f", "n/a"}

    def test_all_entries_have_required_keys(self):
        for entry in LEXICON:
            missing = self.REQUIRED_KEYS - set(entry.keys())
            assert not missing, f"Entry {entry} missing keys: {missing}"

    def test_pos_values_are_valid(self):
        for entry in LEXICON:
            assert entry["pos"] in self.VALID_POS, (
                f"Unknown POS '{entry['pos']}' in entry {entry['laciyo']}"
            )

    def test_gender_values_are_valid(self):
        for entry in LEXICON:
            assert entry["gender"] in self.VALID_GENDER, (
                f"Unknown gender '{entry['gender']}' in entry {entry['laciyo']}"
            )

    def test_english_is_list(self):
        for entry in LEXICON:
            assert isinstance(entry["english"], list), (
                f"'english' should be a list in entry {entry['laciyo']}"
            )

    def test_laciyo_keys_unique(self):
        laciyo_forms = [e["laciyo"] for e in LEXICON]
        # Allow duplicates only when the same form covers multiple POS
        # (e.g. 'libre' is both noun and adj). But Latin keys should be unique.
        latin_forms = [e["latin"] for e in LEXICON]
        assert len(latin_forms) == len(set(latin_forms)), (
            "Duplicate Latin source words in lexicon"
        )


class TestLookup:
    """Tests for the lookup() helper."""

    def test_english_lookup_water(self):
        results = lookup("water")
        assert len(results) >= 1
        laciyo_forms = [r["laciyo"] for r in results]
        assert "akwa" in laciyo_forms

    def test_english_lookup_case_insensitive(self):
        assert lookup("Water") == lookup("water")

    def test_english_lookup_not_found(self):
        assert lookup("xyzzy") == []

    def test_laciyo_lookup_akwa(self):
        entry = lookup("akwa", source="laciyo")
        assert entry is not None
        assert entry["latin"] == "aqua"

    def test_laciyo_lookup_not_found(self):
        assert lookup("zzz", source="laciyo") is None

    def test_latin_lookup_aqua(self):
        entry = lookup("aqua", source="latin")
        assert entry is not None
        assert entry["laciyo"] == "akwa"

    def test_latin_lookup_not_found(self):
        assert lookup("zzz", source="latin") is None

    def test_invalid_source_raises(self):
        with pytest.raises(ValueError, match="Unknown source"):
            lookup("water", source="klingon")

    def test_lookup_english_life(self):
        results = lookup("life", source="english")
        assert any(r["laciyo"] == "vita" for r in results)

    def test_lookup_laciyo_verb(self):
        entry = lookup("ese", source="laciyo")
        assert entry is not None
        assert entry["pos"] == "v"

    def test_lookup_number_one(self):
        results = lookup("one", source="english")
        assert any(r["laciyo"] == "uno" for r in results)
