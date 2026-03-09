"""
laciyo – command-line interface

Usage
-----
    python -m laciyo --help
    python -m laciyo phonology aqua
    python -m laciyo phonology "philosophia et theoria"
    python -m laciyo translate --from latin "aqua vita est"
    python -m laciyo translate --from english water
    python -m laciyo lookup akwa
    python -m laciyo conjugate vedere
    python -m laciyo conjugate vedere --person 1pl
    python -m laciyo pluralise luna
    python -m laciyo phrase ego vedere luna
    python -m laciyo dict --pos n
"""

from __future__ import annotations

import argparse
import json
import sys

from laciyo.phonology import latinise, romanise
from laciyo.lexicon import lookup as lex_lookup
from laciyo.grammar import conjugate, pluralise, full_conjugation
from laciyo.translator import Translator


def _cmd_phonology(args: argparse.Namespace) -> None:
    words = args.text.split()
    result = " ".join(latinise(w) for w in words)
    print(result)


def _cmd_romanise(args: argparse.Namespace) -> None:
    words = args.text.split()
    result = " ".join(romanise(w) for w in words)
    print(result)


def _cmd_translate(args: argparse.Namespace) -> None:
    t = Translator()
    if args.source == "latin":
        print(t.latin_to_laciyo(args.text))
    elif args.source == "english":
        results = t.english_to_laciyo(args.text)
        if results:
            print(", ".join(results))
        else:
            print(f"(no Laciyo word found for '{args.text}')", file=sys.stderr)
            sys.exit(1)
    else:
        results = t.laciyo_to_english(args.text)
        if results:
            print(", ".join(results))
        else:
            print(f"('{args.text}' not found in Laciyo lexicon)", file=sys.stderr)
            sys.exit(1)


def _cmd_lookup(args: argparse.Namespace) -> None:
    entry = lex_lookup(args.word, source="laciyo")
    if entry is None:
        entry = lex_lookup(args.word, source="latin")
    if entry is None:
        entries = lex_lookup(args.word, source="english")
        if entries:
            for e in entries:
                _print_entry(e)
            return
        print(f"('{args.word}' not found)", file=sys.stderr)
        sys.exit(1)
    else:
        _print_entry(entry)


def _print_entry(entry: dict) -> None:
    print(f"  Laciyo : {entry['laciyo']}")
    print(f"  Latin  : {entry['latin']}")
    print(f"  POS    : {entry['pos']}")
    if entry["gender"] != "n/a":
        print(f"  Gender : {entry['gender']}")
    print(f"  English: {', '.join(entry['english'])}")
    if entry["notes"]:
        print(f"  Notes  : {entry['notes']}")


def _cmd_conjugate(args: argparse.Namespace) -> None:
    if args.person:
        form = conjugate(args.infinitive, args.person)
        print(form)
    else:
        paradigm = full_conjugation(args.infinitive)
        labels = {
            "1sg": "I      ",
            "2sg": "you    ",
            "3sg": "he/she ",
            "1pl": "we     ",
            "2pl": "you pl ",
            "3pl": "they   ",
        }
        for key, form in paradigm.items():
            print(f"  {labels[key]}: {form}")


def _cmd_pluralise(args: argparse.Namespace) -> None:
    entry = lex_lookup(args.noun, source="laciyo")
    gender = entry["gender"] if entry and entry["gender"] != "n/a" else "m"
    if args.gender:
        gender = args.gender
    print(pluralise(args.noun, gender))


def _cmd_phrase(args: argparse.Namespace) -> None:
    t = Translator()
    obj = args.obj if args.obj else None
    print(t.phrase(args.subject, args.verb, obj, person=args.person))


def _cmd_dict(args: argparse.Namespace) -> None:
    t = Translator()
    entries = t.dictionary(pos_filter=args.pos)
    for e in entries:
        line = f"{e['laciyo']:18} ({e['pos']}) – {', '.join(e['english'])}"
        print(line)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="laciyo",
        description="Laciyo – Latin Cyber Creole conlang toolkit",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # phonology
    p_phon = sub.add_parser("phonology", help="Convert Latin word(s) to Laciyo spelling")
    p_phon.add_argument("text", help="Latin word or phrase")
    p_phon.set_defaults(func=_cmd_phonology)

    # romanise
    p_rom = sub.add_parser("romanise", help="Convert Laciyo spelling back to approximate Latin")
    p_rom.add_argument("text", help="Laciyo word or phrase")
    p_rom.set_defaults(func=_cmd_romanise)

    # translate
    p_tr = sub.add_parser("translate", help="Translate between Latin/English and Laciyo")
    p_tr.add_argument("text", help="Text to translate")
    p_tr.add_argument(
        "--from",
        dest="source",
        choices=["latin", "english", "laciyo"],
        default="latin",
        help="Source language (default: latin)",
    )
    p_tr.set_defaults(func=_cmd_translate)

    # lookup
    p_lu = sub.add_parser("lookup", help="Look up a word in the Laciyo lexicon")
    p_lu.add_argument("word", help="Word to look up (Laciyo, Latin, or English)")
    p_lu.set_defaults(func=_cmd_lookup)

    # conjugate
    p_conj = sub.add_parser("conjugate", help="Conjugate a Laciyo verb")
    p_conj.add_argument("infinitive", help="Laciyo infinitive (ending in -re)")
    p_conj.add_argument("--person", choices=["1sg", "2sg", "3sg", "1pl", "2pl", "3pl"],
                        help="Person/number (default: full paradigm)")
    p_conj.set_defaults(func=_cmd_conjugate)

    # pluralise
    p_pl = sub.add_parser("pluralise", help="Return the plural form of a Laciyo noun")
    p_pl.add_argument("noun", help="Laciyo singular noun")
    p_pl.add_argument("--gender", choices=["m", "f"], help="Override gender")
    p_pl.set_defaults(func=_cmd_pluralise)

    # phrase
    p_ph = sub.add_parser("phrase", help="Build a simple SVO sentence")
    p_ph.add_argument("subject", help="Laciyo subject (noun or pronoun)")
    p_ph.add_argument("verb", help="Laciyo verb infinitive")
    p_ph.add_argument("obj", nargs="?", help="Optional object noun")
    p_ph.add_argument("--person", default="3sg",
                      choices=["1sg", "2sg", "3sg", "1pl", "2pl", "3pl"])
    p_ph.set_defaults(func=_cmd_phrase)

    # dict
    p_dict = sub.add_parser("dict", help="List the Laciyo dictionary")
    p_dict.add_argument("--pos", help="Filter by part of speech (n, v, adj, …)")
    p_dict.set_defaults(func=_cmd_dict)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
