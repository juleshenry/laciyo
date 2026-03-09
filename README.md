# laciyo
Latin Cyber Creole

**Laciyo** is a constructed language (*conlang*) that reconstitutes Classical
Latin into a simplified, modern, cyberpunk-flavoured creole.  It retains the
unmistakable feel of Latin while shedding the complexity of six cases, three
genders, and irregular declension patterns – making it learnable and usable for
digital communication, speculative fiction, and linguistic exploration.

---

## Design Principles

| Principle | Detail |
|-----------|--------|
| **Latin roots** | All vocabulary is drawn directly from Classical or Late Latin. |
| **Simplified phonology** | Regularised spelling: `qu→kw`, `ph→f`, `th→t`, `x→ks`, `c→s/k`. |
| **Reduced morphology** | Two genders (m/f), two numbers (sg/pl), no case endings. |
| **SVO word order** | Subject – Verb – Object, like modern Romance languages. |
| **Cyber vocabulary** | Technical neologisms coined from Latin roots (e.g. *rete* = network, *kaelo* = cyberspace). |

---

## Phonological Rules (Latin → Laciyo)

Rules applied in order:

1. Macron vowels stripped: `ā→a`, `ē→e`, `ī→i`, `ō→o`, `ū→u`
2. `ph` → `f`  (philosophia → filosofia)
3. `th` → `t`  (theoria → teoria)
4. `qu` → `kw` (aqua → akwa)
5. `x`  → `ks` (rex → reks)
6. `y`  → `i`  (gymnasium → gimnasiu)
7. `cae` → `se`, `coe` → `se` (caelum → selu)
8. `c` before e/i → `s` (cives → sives)
9. remaining `c` → `k` (caro → karo)
10. `ti` before a vowel → `si` (gratia → grasia)
11. Final `-us` → `-o` (dominus → domino)
12. Final `-um` → `-u` (verbum → verbu)
13. Final `-ae` → `-e` (aquae → akwe)
14. Final `-am`/`-em` → `-a`/`-e` (drop nasal)
15. Remaining final `-m` dropped (aquam → akwa)
16. Double consonants simplified (attentio → atensio)

---

## Grammar

### Nouns

| Form | Rule | Example |
|------|------|---------|
| Singular | — | *luna* (moon) |
| Plural (f, -a) | -a → -ae | *lunae* (moons) |
| Plural (m, -o) | -o → -os | *komputos* (computers) |
| Plural (consonant) | + -es | *soles* (suns) |

### Verbs – Present Tense

Infinitive ends in **-re**.  Stem = infinitive minus *-re*, then drop trailing *-e* if present.

| Person | Singular | Plural |
|--------|----------|--------|
| 1st | **-o** | **-amos** |
| 2nd | **-as** | **-atis** |
| 3rd | **-at** | **-ant** |

**Irregular verb: *ese*** (to be)

| Person | Singular | Plural |
|--------|----------|--------|
| 1st | *so* | *samos* |
| 2nd | *es* | *estis* |
| 3rd | *est* | *sont* |

### Adjectives

Invariable for gender.  Plural: add **-s** (vowel stem) or **-es** (consonant stem).

---

## Quick-Start Vocabulary

| Laciyo | Latin | English |
|--------|-------|---------|
| akwa | aqua | water |
| vita | vita | life |
| rete | rete | network / internet |
| kaelo | caelum | sky / cyberspace |
| komputo | computus | computer |
| skriptu | scriptum | script / code |
| makina | machina | machine / device |
| data | data | data |
| muro | murus | wall / firewall |
| libre | liber | free / open |

---

## Python Package

### Installation

```bash
pip install -e .
```

### Programmatic API

```python
from laciyo import Translator, latinise, lookup

# Convert Latin text to Laciyo
t = Translator()
print(t.latin_to_laciyo("verbum vita est"))   # → verbu vita est

# Look up a word
print(lookup("network"))                       # → [{'laciyo': 'rete', ...}]

# Apply phonological rules
print(latinise("philosophia"))                 # → filosofia

# Conjugate a verb
from laciyo import conjugate
print(conjugate("vedere", "1sg"))              # → vedo

# Build a sentence
print(t.phrase("ego", "vedere", "luna", person="1sg"))  # → ego vedo luna.
```

### Command-Line Interface

```bash
# Apply phonological rules
laciyo phonology "aqua philosophia rex"
# → akwa filosofia reks

# Translate a Latin phrase to Laciyo
laciyo translate "aqua vita est" --from latin
# → akwa vita est

# Translate English → Laciyo
laciyo translate network --from english
# → rete

# Look up a word
laciyo lookup akwa

# Conjugate a verb (full paradigm)
laciyo conjugate vedere

# Conjugate a specific person
laciyo conjugate ese --person 3sg
# → est

# Pluralise a noun
laciyo pluralise luna
# → lunae

# Build a sentence
laciyo phrase ego vedere luna --person 1sg
# → ego vedo luna.

# List the dictionary
laciyo dict
laciyo dict --pos v      # verbs only
laciyo dict --pos n      # nouns only
```

---

## Example Sentences

| Laciyo | English |
|--------|---------|
| *Ego so in rete.* | I am on the network. |
| *Komputo vedat data.* | The computer sees/processes data.  |
| *Nos skribemos skriptu libre.* | We write free/open-source code. |
| *Muro kaelo protekat.* | The firewall protects cyberspace. |
| *Akwa vita est.* | Water is life. |
| *Omines et makinae konekteront.* | Humans and machines will connect. |

---

## Project Structure

```
laciyo/
├── laciyo/
│   ├── __init__.py       – public API
│   ├── __main__.py       – CLI entry point
│   ├── phonology.py      – Latin → Laciyo phonological rules
│   ├── lexicon.py        – core vocabulary (~80 entries)
│   ├── grammar.py        – conjugation and pluralisation
│   └── translator.py     – high-level translation interface
├── tests/
│   ├── test_phonology.py
│   ├── test_lexicon.py
│   ├── test_grammar.py
│   ├── test_translator.py
│   └── test_cli.py
├── pyproject.toml
└── setup.py
```

---

## Etymology of the Name

**Laciyo** derives from *Latium* (the region of ancient Rome) via the same
phonological rules the language itself uses:

> *Latium* → *Latio* (us→o) → *Lasio* (ti→si) → *Lasiyo* → **Laciyo**

The final form echoes the *-yo* diminutive/affective suffix found in several
modern Romance and creole languages, marking Laciyo as a living descendant
rather than a museum piece.

