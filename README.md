# Cyber-Latin: A Distributed P2P Language Matrix

Welcome to the **Cyber-Latin** project. This is a global, decentralized effort to mathematically calculate the most efficient, monosyllabic, isolating Romance language possible.

We are treating language creation as an **NP-Complete combinatorial optimization problem**. By combining the lexicons of modern Romance languages (French, Italian, Spanish), we use **Simulated Annealing** across a P2P network of offline contributors to collapse phonetic space and eliminate syllables.

The result will be a beautifully dense, futuristic "Cyber-Latin."

## The Vision
Why build a language with a supercomputer?
Natural languages are full of redundancy. We want a language that prioritizes:
1. **Speed (Minimum Syllables):** Monosyllabic words whenever possible. (*feu* beats *fuego*).
2. **Efficiency (Minimum Phonemes):** Re-using a small inventory of sounds to form isolating roots.
3. **Clarity (Zero Grammatical Collisions):** Stems inside the same grammatical class (like `-ar` verbs) can *never* become homophones.

Because calculating the absolute perfect lexicon across 10,000+ words takes longer than the age of the universe, we need *your* computer to help us find better mathematical minimums.

### Supported Languages (20 Languages, 19 Dumps)

All lexical data is sourced from Wiktionary XML dumps (MediaWiki export v0.11). The corpus spans **20+ GB** of uncompressed XML across **20.8 million pages**.

#### Romance Languages (18 Core)

| Code | Language | Branch | Wiktionary | Dump | Size | Pages |
|------|----------|--------|------------|------|------|------:|
| `fr` | French | Gallo-Romance | Wiktionnaire | full | 7.3 GB | 7,287,012 |
| `es` | Spanish | Ibero-Romance | Wikcionario | full | 967 MB | 982,019 |
| `ca` | Catalan | Occitano-Romance | Viccionari | full | 509 MB | 623,165 |
| `it` | Italian | Italo-Dalmatian | Wikizionario | full | 611 MB | 602,190 |
| `pt` | Portuguese | Ibero-Romance | Wikcionario | full | 561 MB | 555,568 |
| `ro` | Romanian | Eastern Romance | Wikționar | full | 216 MB | 197,244 |
| `gl` | Galician | Ibero-Romance | Wiktionary | full | 109 MB | 104,869 |
| `oc` | Occitan | Occitano-Romance | Wikiccionari | full | 103 MB | 86,776 |
| `ast` | Asturian | Ibero-Romance | Wikcionariu | stub | 55 MB | 77,518 |
| `wa` | Walloon | Gallo-Romance | Wiccionaire | full | 65 MB | 52,490 |
| `la` | Latin | Classical ancestor | Victionarium | full | 68 MB | 49,332 |
| `lmo` | Lombard | Gallo-Italic | Wiktionary | full | 64 MB | 37,855 |
| `scn` | Sicilian | Italo-Dalmatian | Wikizziunariu | full | 30 MB | 23,872 |
| `vec` | Venetian | Gallo-Italic | Wikisionario | full | 9.2 MB | 6,573 |
| `an` | Aragonese | Ibero-Romance | Biquizionario | full | 5.2 MB | 5,450 |
| `rup` | Aromanian | Eastern Romance | Wikționar | full | 1.6 MB | 1,583 |
| `rm` | Romansh | Rhaeto-Romance | Wiktionary | full | 71 KB | 92 |
| `sc` | Sardinian | Insular Romance | Wiktionary | full | 49 KB | 40 |

#### Creoles & Contact Languages (via `enwiktionary` + Incubator)

Languages without standalone Wiktionary dumps, extracted from `==Language==` sections in the English Wiktionary and scraped from the [Wikimedia Incubator](https://incubator.wikimedia.org/wiki/Wt/ht/).

| Code | Language | Base | Branch | Sources |
|------|----------|------|--------|---------|
| `ht` | Haitian Creole | French-based | Atlantic Creole | `enwiktionary`, Incubator (`Wt/ht/`) |

#### Reference Languages (Non-Romance)

| Code | Language | Family | Wiktionary | Dump | Size | Pages |
|------|----------|--------|------------|------|------|------:|
| `en` | English | Germanic | Wiktionary | full | 10 GB | 9,943,880 |

## The Mechanics: How It Works
The entire state of the Cyber-Latin language is stored in a highly compressed binary "genome" file (`.clatin`). 

When you run the node on your machine, it goes offline and begins a **Simulated Annealing** loop:
* It randomly swaps out word choices (e.g., swapping *rojo* for *rouge*).
* It recalculates the total "Energy" score of the language `(Energy = 1000 * Syllables + 10 * Phonemes + 100,000 * Grammar Collisions)`.
* It repeats this millions of times, slowly "cooling" down until it finds a localized mathematical floor.

## How to Contribute (The P2P Node)

### 1. Download and Run
1. Download the latest `cyberlatin-cli` executable for your system.
2. Download the current community baseline: `genesis.clatin`.
3. Run the engine offline:
   ```bash
   cyberlatin start genesis.clatin
   ```
4. Let your computer churn. It will output a new file: `local_optimal.clatin` along with its Energy Score. **Lower is better.**

### 2. Share and Merge
If your `local_optimal.clatin` achieves a lower Energy Score than the current global baseline, **you have advanced the language!**
* Share your `.clatin` file with the community (via GitHub PR, Discord, IPFS, or email).
* To merge someone else's file and check if they beat your score:
  ```bash
  cyberlatin merge peer_file.clatin
  ```
  If their score is lower, your node will permanently adopt their genome as the new baseline.

Join the grid. Let's calculate a language.

## Roadmap: From Grammar to Literature

The development of Cyber-Latin (Lacyo) will follow a phased, methodical progression. We build from the mathematical and grammatical foundations up to complex literature and cultural expressions.

### Phase 0: Grammar Consolidation
Establish the definitive mathematical and structural constraints of the language.
* **Outputs:** `docs/grammar/grammar.tex` (Reference specification) and accompanying codebase structures.
* **Content:** Stemming selection rules, morpheme agglutination phases, global phoneme inventory, and collision avoidance logic.

### Phase 1: Total Lexical Development
Execute the simulated annealing engine across the full Wiktionary database.
* **Outputs:** A stable, comprehensive `.clatin` genome covering a core 5,000+ word vocabulary.
* **Content:** Extraction, scoring, and selection of words from French, Spanish, Italian, Portuguese, Romanian, etc.

### Phase 2: Idioms & Phraseology
Map the rich, multivaried idiomatic expressions of all base Romance languages into Cyber-Latin.
* **Outputs:** `books/idioms/idioms.tex` (A comprehensive phrasebook).
* **Content:** Translating metaphorical structures while adhering to agglutinative rules.

### Phase 3: Text-Talk & Slang Guide
Adapt internet chat conventions and abbreviations from modern Romance languages into a standardized Cyber-Latin digital shorthand.
* **Outputs:** `books/text-talk/text-talk.tex` (A digital phrasebook/guide).
* **Content:** Mapping "jaja" (ES), "rsrs" / "kkk" (PT), "mdr" (FR) to their mathematical equivalents.

### Phase 4: Children's Book
A simple, engaging narrative to demonstrate basic syntax and everyday vocabulary.
* **Outputs:** `books/kids-book/kids-book.tex`.
* **Content:** Original narrative focusing on elemental concepts.

### Phase 5: Beginner's Didactic Guide
A teaching resource using structured passages to introduce readers to the language systematically.
* **Outputs:** `books/beginners-guide/beginners-guide.tex`.
* **Content:** Gradual vocabulary introduction, grammar exercises, and annotated texts.

### Phase 6: Core Translations (Foundational Texts)
Translating culturally significant foundational works.
* **Outputs:** `books/bible/bible.tex` (Full Bible translation).

### Phase 7: World Literature Expansion
Demonstrating the expressive capacity of Cyber-Latin across diverse literary styles from all major Romance branches, plus global classics.
* **Alice in Wonderland:** `books/alice/alice.tex` (Full novel)
* **Dante's Inferno (Italian):** `books/inferno/inferno.tex` (Selected cantos or full)
* **Don Quixote (Spanish):** `books/don-quixote/don-quixote.tex`
* **Os Lusiadas (Portuguese):** `books/lusiadas/lusiadas.tex`
* **Le Petit Prince (French):** `books/petit-prince/petit-prince.tex`
* **Miorita (Romanian):** `books/miorita/miorita.tex`
