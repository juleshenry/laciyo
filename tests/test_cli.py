"""Tests for laciyo CLI (__main__)"""

import pytest
from laciyo.__main__ import build_parser, main


class TestCLIParse:
    def test_phonology_command(self, capsys):
        main(["phonology", "aqua"])
        out = capsys.readouterr().out.strip()
        assert out == "akwa"

    def test_phonology_phrase(self, capsys):
        main(["phonology", "verbum"])
        out = capsys.readouterr().out.strip()
        assert out == "verbu"

    def test_translate_latin(self, capsys):
        main(["translate", "aqua", "--from", "latin"])
        out = capsys.readouterr().out.strip()
        assert out == "akwa"

    def test_translate_english(self, capsys):
        main(["translate", "water", "--from", "english"])
        out = capsys.readouterr().out.strip()
        assert "akwa" in out

    def test_translate_laciyo(self, capsys):
        main(["translate", "akwa", "--from", "laciyo"])
        out = capsys.readouterr().out.strip()
        assert "water" in out

    def test_lookup_laciyo(self, capsys):
        main(["lookup", "akwa"])
        out = capsys.readouterr().out
        assert "aqua" in out

    def test_conjugate_full_paradigm(self, capsys):
        main(["conjugate", "vedere"])
        out = capsys.readouterr().out
        assert "vedo" in out
        assert "vedas" in out

    def test_conjugate_single_person(self, capsys):
        main(["conjugate", "vedere", "--person", "1sg"])
        out = capsys.readouterr().out.strip()
        assert out == "vedo"

    def test_pluralise_noun(self, capsys):
        main(["pluralise", "luna"])
        out = capsys.readouterr().out.strip()
        assert out == "lunae"

    def test_phrase_command(self, capsys):
        main(["phrase", "ego", "vedere", "luna", "--person", "1sg"])
        out = capsys.readouterr().out.strip()
        assert out == "ego vedo luna."

    def test_dict_command(self, capsys):
        main(["dict"])
        out = capsys.readouterr().out
        assert "akwa" in out

    def test_dict_pos_filter(self, capsys):
        main(["dict", "--pos", "v"])
        out = capsys.readouterr().out
        assert "(v)" in out
        assert "(n)" not in out

    def test_translate_not_found_exits(self):
        with pytest.raises(SystemExit) as exc:
            main(["translate", "xyzzy", "--from", "english"])
        assert exc.value.code == 1
