# Lacyo

A constructed language derived from computational optimization over the Romance
language family. Lacyo uses simulated annealing to discover optimal roots,
fusional endings, and phoneme inventory by minimizing a multi-term energy
function across ~3000 concepts extracted from French, Spanish, Italian, and
Portuguese.

## Architecture

```
Python prep (G2P)  →  JSON candidates  →  Rust SA optimizer  →  JSON lexicon
   lacyo/                data/              cyberlatin-cli/         data/
```

**Python** handles phonological data preparation (epitran G2P is Python-only).
**Rust** handles the simulated annealing hot loop (millions of iterations in
seconds).

## Quick Start

```bash
# 1. Python prep: extract top-1000 words, IPA transcription, candidate building
.venv/bin/python3 -m lacyo.pipeline prep -n 1000 -o data/candidates.json

# 2. Rust optimizer: simulated annealing over candidates
cd cyberlatin-cli && cargo build --release && cd ..
./cyberlatin-cli/target/release/cyberlatin-cli \
    -i data/candidates.json \
    -o data/lacyo_lexicon.json \
    -n 2000000

# Output: data/lacyo_lexicon.json (lexicon + endings + phoneme inventory)
```

## Energy Function

The optimizer minimizes:

```
E = w_syl  · Σ syllables(root_i)       # prefer short roots
  + w_phon · |Φ|                        # minimize phoneme inventory size
  + w_end  · Σ syllables(ending_j)      # prefer short endings
  + w_coll · collisions                 # no duplicate endings in a paradigm
  + w_tact · violations                 # phonotactic well-formedness
  + w_dist · distinctiveness_penalty    # endings must be perceptually distinct
```

The phoneme inventory is **emergent** — the 23-phoneme set (18C + 5V) is the
search space ceiling. Whichever phonemes survive in the optimized roots become
the actual inventory. `E_phon` pressures the optimizer to use fewer phonemes.

## Phonotactics

Naturalistic, respecting Romance source material:
- Any single consonant is a legal coda
- Coda clusters up to 2 allowed if sonorant precedes obstruent (e.g. /ns/, /nd/, /rt/)
- Onset clusters: obstruent + liquid/glide (e.g. /pl/, /tr/, /kw/)
- No gemination across syllable boundaries
- Diphthongs are unit phonemes

## Fusional Morphology

Latin-style fusional endings encode multiple grammatical features simultaneously:
- **Nouns:** 6 slots (nom/acc/gen × sg/pl)
- **Verbs:** 3 tenses × 3 persons × 2 numbers × 2 moods + inf/participles/imperatives
- **Adjectives:** sg/pl

Endings are optimized alongside roots to maximize distinctiveness within paradigms.

## Project Structure

```
lacyo/                  Python package
  phonology.py          IPA tokenization, G2P, phonotactics, orthography
  optimizer.py          Python SA (testing only, too slow for production)
  pipeline.py           E2E pipeline: prep (export JSON) and run (full Python)

cyberlatin-cli/         Rust SA optimizer
  src/lib.rs            Core types, energy function, mutation, incremental cache
  src/main.rs           CLI, progress bar, SA loop, summary output

data/                   Pipeline I/O
  candidates.json       Python prep output → Rust input
  lacyo_lexicon.json    Optimizer output (roots + endings + inventory)
  latin_morphemes.json  Canonical morpheme database

docs/grammar/
  grammar.tex           Full language specification (~900 lines)

xmls/                   Wiktionary dumps (not tracked in git)
```

## Spec

The canonical language specification is in `docs/grammar/grammar.tex`. It covers
phonology, morphology, the energy function, pipeline architecture, syntax,
worked examples, and open questions.
