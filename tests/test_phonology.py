"""Tests for laciyo.phonology"""

import pytest
from laciyo.phonology import latinise, romanise


class TestLatinise:
    """Unit tests for the Latin → Laciyo phonological mapping."""

    def test_aqua(self):
        assert latinise("aqua") == "akwa"

    def test_verbum(self):
        assert latinise("verbum") == "verbu"

    def test_philosophia(self):
        assert latinise("philosophia") == "filosofia"

    def test_rex(self):
        assert latinise("rex") == "reks"

    def test_gratia(self):
        # ti before vowel → si
        assert latinise("gratia") == "grasia"

    def test_nox(self):
        assert latinise("nox") == "noks"

    def test_lux(self):
        assert latinise("lux") == "luks"

    def test_theoria(self):
        assert latinise("theoria") == "teoria"

    def test_quinque(self):
        # qu → kw twice: q-u-i-n-q-u-e → kw-i-n-kw-e
        assert latinise("quinque") == "kwinkwe"

    def test_terminus_us(self):
        # -us → -o
        assert latinise("dominus") == "domino"

    def test_terminus_um(self):
        # -um → -u
        assert latinise("scriptum") == "skriptu"

    def test_terminus_ae(self):
        # -ae → -e
        assert latinise("aquae") == "akwe"

    def test_drop_final_m(self):
        # final -m dropped
        assert latinise("aquam") == "akwa"

    def test_caelum(self):
        # cae → se, then um → u
        assert latinise("caelum") == "selu"

    def test_double_consonant_simplification(self):
        # tt → t
        assert latinise("attentio") == "atensio"

    def test_macron_stripped(self):
        assert latinise("ā") == "a"
        assert latinise("ūnus") == "uno"

    def test_case_insensitive_rules(self):
        # Rules should handle upper-case input
        result = latinise("AQUA")
        assert result.lower() == "akwa"

    def test_unchanged_word(self):
        # A word with no transformable patterns comes through unchanged
        assert latinise("sol") == "sol"

    def test_vita(self):
        assert latinise("vita") == "vita"

    def test_luna(self):
        assert latinise("luna") == "luna"


class TestRomanise:
    """Unit tests for the Laciyo → approximate Latin reverse mapping."""

    def test_akwa_to_aqua(self):
        assert romanise("akwa") == "aqua"

    def test_verbu_to_verbum(self):
        result = romanise("verbu")
        assert "verb" in result

    def test_reks_to_rex(self):
        result = romanise("reks")
        assert result == "rex"

    def test_roundtrip_approximate(self):
        # Round-trip is not exact but the key sounds should survive
        original = "aqua"
        laciyo = latinise(original)
        back = romanise(laciyo)
        # Should contain the root 'aqu'
        assert "aqu" in back
