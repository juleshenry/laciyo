//! lacyo phonology & energy function — core types and optimizer logic.
//!
//! Implements the grammar.tex Ch.2 phonotactics and Ch.4 energy function
//! operating on IPA phoneme sequences (not orthographic characters).

use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

// ── Lacyo phoneme inventory (grammar.tex Ch.2) ──────────────────────────

pub const VOWELS: &[&str] = &["a", "e", "i", "o", "u"];

pub const CONSONANTS: &[&str] = &[
    "p", "b", "t", "d", "k", "ɡ",
    "m", "n",
    "f", "v", "s", "z", "ʃ",
    "t͡ʃ",
    "l", "r",
    "j", "w",
];

pub const LEGAL_CODAS: &[&str] = &["n", "s", "r", "l"];

pub const OBSTRUENTS: &[&str] = &["p", "b", "t", "d", "k", "ɡ", "f", "v", "s"];

pub const ONSET2: &[&str] = &["l", "r", "j", "w"];

// ── IPA → orthography ───────────────────────────────────────────────────

pub fn ipa_to_ortho(phoneme: &str) -> &str {
    match phoneme {
        "p" => "p", "b" => "b", "t" => "t", "d" => "d", "k" => "k", "ɡ" => "g",
        "m" => "m", "n" => "n",
        "f" => "f", "v" => "v", "s" => "s", "z" => "z",
        "ʃ" => "x", "t͡ʃ" => "c",
        "l" => "l", "r" => "r",
        "j" => "y", "w" => "w",
        "a" => "a", "e" => "e", "i" => "i", "o" => "o", "u" => "u",
        _ => "?",
    }
}

pub fn phonemes_to_ortho(seq: &[String]) -> String {
    seq.iter().map(|p| ipa_to_ortho(p)).collect()
}

// ── Helper predicates ───────────────────────────────────────────────────

#[inline]
pub fn is_vowel(p: &str) -> bool {
    VOWELS.contains(&p)
}

#[inline]
pub fn is_consonant(p: &str) -> bool {
    !is_vowel(p)
}

#[inline]
pub fn is_legal_coda(p: &str) -> bool {
    LEGAL_CODAS.contains(&p)
}

#[inline]
pub fn is_obstruent(p: &str) -> bool {
    OBSTRUENTS.contains(&p)
}

#[inline]
pub fn is_onset2(p: &str) -> bool {
    ONSET2.contains(&p)
}

// ── Syllable counting (IPA-based) ───────────────────────────────────────

pub fn count_syllables(seq: &[String]) -> u32 {
    let c = seq.iter().filter(|p| is_vowel(p)).count() as u32;
    c.max(1)
}

// ── Phonotactic violation counting ──────────────────────────────────────

/// Syllabify using maximal onset principle. Returns Vec of syllables,
/// each syllable a Vec of phoneme indices into `seq`.
fn syllabify(seq: &[String]) -> Vec<Vec<usize>> {
    if seq.is_empty() {
        return vec![];
    }

    let vowel_positions: Vec<usize> = seq.iter()
        .enumerate()
        .filter(|(_, p)| is_vowel(p))
        .map(|(i, _)| i)
        .collect();

    if vowel_positions.is_empty() {
        return vec![(0..seq.len()).collect()];
    }

    let mut syllables: Vec<Vec<usize>> = Vec::new();

    for (si, &vi) in vowel_positions.iter().enumerate() {
        let start;
        if si == 0 {
            start = 0;
        } else {
            let prev_vi = vowel_positions[si - 1];
            let inter_start = prev_vi + 1;
            let inter_len = vi - inter_start;

            if inter_len == 0 {
                start = vi;
            } else if inter_len == 1 {
                start = inter_start;
            } else if inter_len == 2 {
                let c1 = &seq[inter_start];
                let c2 = &seq[inter_start + 1];
                if is_obstruent(c1) && is_onset2(c2) {
                    start = inter_start;
                } else {
                    syllables.last_mut().unwrap().push(inter_start);
                    start = inter_start + 1;
                }
            } else {
                let c_pen = &seq[vi - 2];
                let c_last = &seq[vi - 1];
                if is_obstruent(c_pen) && is_onset2(c_last) {
                    for idx in inter_start..(vi - 2) {
                        syllables.last_mut().unwrap().push(idx);
                    }
                    start = vi - 2;
                } else {
                    for idx in inter_start..(vi - 1) {
                        syllables.last_mut().unwrap().push(idx);
                    }
                    start = vi - 1;
                }
            }
        }

        let end = vi + 1; // just the vowel nucleus; trailing handled later
        let syl: Vec<usize> = (start..end).collect();
        syllables.push(syl);
    }

    // Trailing consonants after last vowel
    let last_vi = *vowel_positions.last().unwrap();
    if last_vi + 1 < seq.len() {
        for idx in (last_vi + 1)..seq.len() {
            syllables.last_mut().unwrap().push(idx);
        }
    }

    syllables
}

pub fn count_violations(seq: &[String]) -> u32 {
    let mut violations = 0u32;
    let syls = syllabify(seq);

    for syl_indices in &syls {
        let syl: Vec<&str> = syl_indices.iter().map(|&i| seq[i].as_str()).collect();

        // Find vowel nucleus
        let nuc_pos = syl.iter().position(|p| is_vowel(p));
        let nuc_idx = match nuc_pos {
            Some(i) => i,
            None => { violations += 1; continue; }
        };

        let onset = &syl[..nuc_idx];
        let coda = &syl[nuc_idx + 1..];

        // No coda clusters
        if coda.len() > 1 {
            violations += (coda.len() - 1) as u32;
        }

        // No onset triples
        if onset.len() > 2 {
            violations += (onset.len() - 2) as u32;
        }

        // Onset cluster rule
        if onset.len() == 2 {
            if !is_obstruent(onset[0]) || !is_onset2(onset[1]) {
                violations += 1;
            }
        }

        // Coda constraint
        for c in coda {
            if !is_legal_coda(c) {
                violations += 1;
            }
        }
    }

    // No gemination across syllable boundaries
    for i in 0..syls.len().saturating_sub(1) {
        let last_of_prev = syls[i].last().map(|&idx| &seq[idx]);
        let first_of_next = syls[i + 1].first().map(|&idx| &seq[idx]);
        if let (Some(a), Some(b)) = (last_of_prev, first_of_next) {
            if a == b && is_consonant(a) {
                violations += 1;
            }
        }
    }

    // NOTE: No hard inventory membership check here.
    // The phoneme inventory is EMERGENT — it's whatever phonemes the
    // optimizer ends up using. The 23-phoneme set is just the candidate
    // ceiling enforced during Python G2P adaptation. E_phon penalizes
    // inventory size, not membership.

    violations
}

// ── Phonemic edit distance ──────────────────────────────────────────────

pub fn phonemic_edit_distance(a: &[String], b: &[String]) -> u32 {
    let m = a.len();
    let n = b.len();
    let mut dp = vec![0u32; n + 1];
    for j in 0..=n { dp[j] = j as u32; }

    for i in 1..=m {
        let mut prev = dp[0];
        dp[0] = i as u32;
        for j in 1..=n {
            let tmp = dp[j];
            if a[i - 1] == b[j - 1] {
                dp[j] = prev;
            } else {
                dp[j] = 1 + prev.min(dp[j]).min(dp[j - 1]);
            }
            prev = tmp;
        }
    }
    dp[n]
}

// ── Data structures (JSON interchange with Python) ──────────────────────

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct CandidateData {
    pub concept: String,
    pub source_lang: String,
    pub source_word: String,
    pub ipa: String,
    pub lacyo_phonemes: Vec<String>,
    pub orthography: String,
    pub syllables: u32,
    pub violations: u32,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct PipelineInput {
    pub concepts: HashMap<String, Vec<CandidateData>>,
}

// ── Ending paradigm slots ───────────────────────────────────────────────

pub const NOUN_SLOTS: &[&str] = &[
    "nom_sg", "nom_pl", "acc_sg", "acc_pl", "gen_sg", "gen_pl",
];

pub fn verb_slots() -> Vec<String> {
    let mut slots = Vec::new();
    for tense in &["prs", "pst", "fut"] {
        for person in &["1", "2", "3"] {
            for number in &["sg", "pl"] {
                slots.push(format!("{}_{}{}",  tense, person, number));
            }
        }
    }
    for tense in &["prs", "pst", "fut"] {
        for person in &["1", "2", "3"] {
            for number in &["sg", "pl"] {
                slots.push(format!("{}_subj_{}{}", tense, person, number));
            }
        }
    }
    slots.extend(["inf", "ptcp_act", "ptcp_pas", "imp_2sg", "imp_2pl"]
        .iter().map(|s| s.to_string()));
    slots
}

pub const ADJ_SLOTS: &[&str] = &["sg", "pl"];

// ── Legal endings pool ──────────────────────────────────────────────────

pub fn generate_legal_endings() -> Vec<Vec<String>> {
    let mut endings: Vec<Vec<String>> = Vec::new();
    let vowels = VOWELS;
    let codas = LEGAL_CODAS;
    // Use a subset of consonants as onsets (skip w for endings)
    let onsets: Vec<&str> = CONSONANTS.iter()
        .filter(|&&c| c != "w")
        .copied()
        .collect();

    // V
    for &v in vowels {
        endings.push(vec![v.to_string()]);
    }
    // CV
    for &c in &onsets {
        for &v in vowels {
            endings.push(vec![c.to_string(), v.to_string()]);
        }
    }
    // VC
    for &v in vowels {
        for &cd in codas {
            endings.push(vec![v.to_string(), cd.to_string()]);
        }
    }
    // CVC
    for &c in &onsets {
        for &v in vowels {
            for &cd in codas {
                endings.push(vec![c.to_string(), v.to_string(), cd.to_string()]);
            }
        }
    }

    endings
}

// ── Genome state ────────────────────────────────────────────────────────

#[derive(Clone)]
pub struct Genome {
    /// concept_id → index into candidates
    pub selections: Vec<usize>,
    /// concept_ids in order (parallel to selections)
    pub concept_ids: Vec<String>,
    /// concept_id → candidates list
    pub candidates: HashMap<String, Vec<CandidateData>>,
    /// Noun endings: class → slot → phoneme seq
    pub noun_endings: Vec<Vec<Vec<String>>>,   // [class][slot][phonemes]
    /// Verb endings: class → slot → phoneme seq
    pub verb_endings: Vec<Vec<Vec<String>>>,
    /// Adj endings: slot → phoneme seq
    pub adj_endings: Vec<Vec<String>>,
}

impl Genome {
    pub fn get_root(&self, idx: usize) -> &CandidateData {
        let cid = &self.concept_ids[idx];
        let sel = self.selections[idx];
        &self.candidates[cid][sel]
    }

    pub fn n_concepts(&self) -> usize {
        self.concept_ids.len()
    }
}

// ── Energy weights (grammar.tex Ch.4) ───────────────────────────────────

pub const W_SYL: f64  = 1000.0;
pub const W_PHON: f64 = 50.0;
pub const W_END: f64  = 200.0;
pub const W_COLL: f64 = 100_000.0;
pub const W_TACT: f64 = 500_000.0;
pub const W_DIST: f64 = 500.0;
pub const DIST_THRESHOLD: u32 = 2;

#[derive(Clone, Debug, Serialize)]
pub struct EnergyBreakdown {
    pub e_root: f64,
    pub e_phon: f64,
    pub e_end: f64,
    pub e_coll: f64,
    pub e_tact: f64,
    pub e_dist: f64,
    pub total: f64,
}

pub fn compute_energy(genome: &Genome) -> EnergyBreakdown {
    // E_root
    let mut root_syls = 0u64;
    let mut all_phonemes: HashSet<String> = HashSet::new();
    let mut root_viols = 0u64;

    for i in 0..genome.n_concepts() {
        let r = genome.get_root(i);
        root_syls += r.syllables as u64;
        root_viols += r.violations as u64;
        for p in &r.lacyo_phonemes {
            all_phonemes.insert(p.clone());
        }
    }
    let e_root = W_SYL * root_syls as f64;

    // Collect ending phonemes
    let mut end_syls = 0u64;
    let mut end_viols = 0u64;

    let all_ending_seqs = collect_all_endings(genome);
    for seq in &all_ending_seqs {
        end_syls += count_syllables(seq) as u64;
        end_viols += count_violations(seq) as u64;
        for p in *seq {
            all_phonemes.insert(p.clone());
        }
    }

    let e_phon = W_PHON * all_phonemes.len() as f64;
    let e_end = W_END * end_syls as f64;
    let e_tact = W_TACT * (root_viols + end_viols) as f64;

    // Collisions within paradigms
    let mut collisions = 0u64;
    for cls in &genome.noun_endings {
        for i in 0..cls.len() {
            for j in (i + 1)..cls.len() {
                if cls[i] == cls[j] {
                    collisions += 1;
                }
            }
        }
    }
    for cls in &genome.verb_endings {
        for i in 0..cls.len() {
            for j in (i + 1)..cls.len() {
                if cls[i] == cls[j] {
                    collisions += 1;
                }
            }
        }
    }
    for i in 0..genome.adj_endings.len() {
        for j in (i + 1)..genome.adj_endings.len() {
            if genome.adj_endings[i] == genome.adj_endings[j] {
                collisions += 1;
            }
        }
    }
    let e_coll = W_COLL * collisions as f64;

    // Distinctiveness: only check noun + adj paradigms fully,
    // verb paradigm check within groups of 6 (same tense)
    let mut dist_penalty = 0.0f64;
    for cls in &genome.noun_endings {
        for i in 0..cls.len() {
            for j in (i + 1)..cls.len() {
                let d = phonemic_edit_distance(&cls[i], &cls[j]);
                if d < DIST_THRESHOLD {
                    dist_penalty += (DIST_THRESHOLD - d) as f64;
                }
            }
        }
    }
    for cls in &genome.verb_endings {
        // Check within groups of 6 (one tense × all person/number)
        let group_size = 6;
        let n_groups = (cls.len() + group_size - 1) / group_size;
        for g in 0..n_groups {
            let start = g * group_size;
            let end = (start + group_size).min(cls.len());
            for i in start..end {
                for j in (i + 1)..end {
                    let d = phonemic_edit_distance(&cls[i], &cls[j]);
                    if d < DIST_THRESHOLD {
                        dist_penalty += (DIST_THRESHOLD - d) as f64;
                    }
                }
            }
        }
    }
    for i in 0..genome.adj_endings.len() {
        for j in (i + 1)..genome.adj_endings.len() {
            let d = phonemic_edit_distance(&genome.adj_endings[i], &genome.adj_endings[j]);
            if d < DIST_THRESHOLD {
                dist_penalty += (DIST_THRESHOLD - d) as f64;
            }
        }
    }
    let e_dist = W_DIST * dist_penalty;

    let total = e_root + e_phon + e_end + e_coll + e_tact + e_dist;

    EnergyBreakdown { e_root, e_phon, e_end, e_coll, e_tact, e_dist, total }
}

fn collect_all_endings(genome: &Genome) -> Vec<&Vec<String>> {
    let mut out: Vec<&Vec<String>> = Vec::new();
    for cls in &genome.noun_endings {
        for seq in cls {
            out.push(seq);
        }
    }
    for cls in &genome.verb_endings {
        for seq in cls {
            out.push(seq);
        }
    }
    for seq in &genome.adj_endings {
        out.push(seq);
    }
    out
}

// ── Genome initialization ───────────────────────────────────────────────

pub fn init_genome(
    input: &PipelineInput,
    legal_endings: &[Vec<String>],
    rng: &mut impl rand::Rng,
) -> Genome {
    let concept_ids: Vec<String> = input.concepts.keys().cloned().collect();
    let mut selections = Vec::with_capacity(concept_ids.len());

    for cid in &concept_ids {
        let cands = &input.concepts[cid];
        // Prefer legal (violations==0), then shortest
        let best = cands.iter()
            .enumerate()
            .min_by_key(|(_, c)| (c.violations, c.syllables))
            .map(|(i, _)| i)
            .unwrap_or(0);
        selections.push(best);
    }

    let v_slots = verb_slots();

    // 1 noun class, 1 verb class
    let noun_endings = vec![
        NOUN_SLOTS.iter().map(|_| random_ending(legal_endings, rng)).collect()
    ];
    let verb_endings = vec![
        v_slots.iter().map(|_| random_ending(legal_endings, rng)).collect()
    ];
    let adj_endings: Vec<Vec<String>> = ADJ_SLOTS.iter()
        .map(|_| random_ending(legal_endings, rng))
        .collect();

    Genome {
        selections,
        concept_ids,
        candidates: input.concepts.clone(),
        noun_endings,
        verb_endings,
        adj_endings,
    }
}

fn random_ending(pool: &[Vec<String>], rng: &mut impl rand::Rng) -> Vec<String> {
    pool[rng.gen_range(0..pool.len())].clone()
}

// ── Mutations ───────────────────────────────────────────────────────────

pub fn mutate(
    genome: &mut Genome,
    legal_endings: &[Vec<String>],
    rng: &mut impl rand::Rng,
) {
    if rng.gen_bool(0.5) {
        mutate_root(genome, rng);
    } else {
        mutate_ending(genome, legal_endings, rng);
    }
}

fn mutate_root(genome: &mut Genome, rng: &mut impl rand::Rng) {
    let n = genome.n_concepts();
    if n == 0 { return; }
    let idx = rng.gen_range(0..n);
    let cid = &genome.concept_ids[idx];
    let n_cands = genome.candidates[cid].len();
    if n_cands <= 1 { return; }
    let old = genome.selections[idx];
    let mut new_sel = old;
    while new_sel == old {
        new_sel = rng.gen_range(0..n_cands);
    }
    genome.selections[idx] = new_sel;
}

fn mutate_ending(
    genome: &mut Genome,
    legal_endings: &[Vec<String>],
    rng: &mut impl rand::Rng,
) {
    let r: f64 = rng.gen();
    if r < 0.15 {
        // Noun ending
        let cls = rng.gen_range(0..genome.noun_endings.len());
        let slot = rng.gen_range(0..genome.noun_endings[cls].len());
        genome.noun_endings[cls][slot] = random_ending(legal_endings, rng);
    } else if r < 0.95 {
        // Verb ending
        let cls = rng.gen_range(0..genome.verb_endings.len());
        let slot = rng.gen_range(0..genome.verb_endings[cls].len());
        genome.verb_endings[cls][slot] = random_ending(legal_endings, rng);
    } else {
        // Adj ending
        let slot = rng.gen_range(0..genome.adj_endings.len());
        genome.adj_endings[slot] = random_ending(legal_endings, rng);
    }
}

// ── Output format ───────────────────────────────────────────────────────

#[derive(Serialize)]
pub struct LexiconOutput {
    pub version: String,
    pub metadata: OutputMetadata,
    pub energy_breakdown: EnergyBreakdown,
    pub phoneme_inventory: Vec<String>,
    pub phoneme_count: usize,
    pub roots: HashMap<String, RootOutput>,
    pub noun_endings: HashMap<String, HashMap<String, String>>,
    pub verb_endings: HashMap<String, HashMap<String, String>>,
    pub adj_endings: HashMap<String, String>,
}

#[derive(Serialize)]
pub struct OutputMetadata {
    pub total_concepts: usize,
    pub total_energy: f64,
    pub iterations: u64,
    pub acceptance_rate: f64,
}

#[derive(Serialize)]
pub struct RootOutput {
    pub ipa: Vec<String>,
    pub orthography: String,
    pub source_lang: String,
    pub source_word: String,
    pub syllables: u32,
    pub violations: u32,
}

pub fn format_output(
    genome: &Genome,
    breakdown: &EnergyBreakdown,
    iterations: u64,
    accepted: u64,
) -> LexiconOutput {
    let mut all_phonemes: HashSet<String> = HashSet::new();
    let mut roots: HashMap<String, RootOutput> = HashMap::new();

    for i in 0..genome.n_concepts() {
        let r = genome.get_root(i);
        for p in &r.lacyo_phonemes {
            all_phonemes.insert(p.clone());
        }
        roots.insert(genome.concept_ids[i].clone(), RootOutput {
            ipa: r.lacyo_phonemes.clone(),
            orthography: r.orthography.clone(),
            source_lang: r.source_lang.clone(),
            source_word: r.source_word.clone(),
            syllables: r.syllables,
            violations: r.violations,
        });
    }

    // Noun endings
    let mut noun_out: HashMap<String, HashMap<String, String>> = HashMap::new();
    for (ci, cls) in genome.noun_endings.iter().enumerate() {
        let mut m = HashMap::new();
        for (si, seq) in cls.iter().enumerate() {
            for p in seq { all_phonemes.insert(p.clone()); }
            let slot_name = NOUN_SLOTS.get(si).unwrap_or(&"?");
            m.insert(slot_name.to_string(), phonemes_to_ortho(seq));
        }
        noun_out.insert(format!("class_{}", ci + 1), m);
    }

    // Verb endings
    let v_slots = verb_slots();
    let mut verb_out: HashMap<String, HashMap<String, String>> = HashMap::new();
    for (ci, cls) in genome.verb_endings.iter().enumerate() {
        let mut m = HashMap::new();
        for (si, seq) in cls.iter().enumerate() {
            for p in seq { all_phonemes.insert(p.clone()); }
            let slot_name = v_slots.get(si).map(|s| s.as_str()).unwrap_or("?");
            m.insert(slot_name.to_string(), phonemes_to_ortho(seq));
        }
        verb_out.insert(format!("class_{}", ci + 1), m);
    }

    // Adj endings
    let mut adj_out: HashMap<String, String> = HashMap::new();
    for (si, seq) in genome.adj_endings.iter().enumerate() {
        for p in seq { all_phonemes.insert(p.clone()); }
        let slot_name = ADJ_SLOTS.get(si).unwrap_or(&"?");
        adj_out.insert(slot_name.to_string(), phonemes_to_ortho(seq));
    }

    let mut phon_sorted: Vec<String> = all_phonemes.into_iter().collect();
    phon_sorted.sort();

    LexiconOutput {
        version: "2.0".to_string(),
        metadata: OutputMetadata {
            total_concepts: genome.n_concepts(),
            total_energy: breakdown.total,
            iterations,
            acceptance_rate: if iterations > 0 { accepted as f64 / iterations as f64 } else { 0.0 },
        },
        energy_breakdown: breakdown.clone(),
        phoneme_inventory: phon_sorted.clone(),
        phoneme_count: phon_sorted.len(),
        roots,
        noun_endings: noun_out,
        verb_endings: verb_out,
        adj_endings: adj_out,
    }
}

// ── Tests ───────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_syllables_ipa() {
        // "rux" = /r u ʃ/ → 1 vowel → 1 syllable
        let seq: Vec<String> = vec!["r", "u", "ʃ"].into_iter().map(String::from).collect();
        assert_eq!(count_syllables(&seq), 1);

        // "akwa" = /a k w a/ → 2 vowels → 2 syllables
        let seq: Vec<String> = vec!["a", "k", "w", "a"].into_iter().map(String::from).collect();
        assert_eq!(count_syllables(&seq), 2);
    }

    #[test]
    fn test_violations_clean() {
        // CV.CV = "ta.re" → 0 violations
        let seq: Vec<String> = vec!["t", "a", "r", "e"].into_iter().map(String::from).collect();
        assert_eq!(count_violations(&seq), 0);
    }

    #[test]
    fn test_violations_bad_coda() {
        // "ak" → coda /k/ is not legal
        let seq: Vec<String> = vec!["a", "k"].into_iter().map(String::from).collect();
        assert!(count_violations(&seq) > 0);
    }

    #[test]
    fn test_edit_distance() {
        let a: Vec<String> = vec!["a", "s"].into_iter().map(String::from).collect();
        let b: Vec<String> = vec!["a", "n"].into_iter().map(String::from).collect();
        assert_eq!(phonemic_edit_distance(&a, &b), 1);
    }

    #[test]
    fn test_ortho() {
        let seq: Vec<String> = vec!["t͡ʃ", "a"].into_iter().map(String::from).collect();
        assert_eq!(phonemes_to_ortho(&seq), "ca");
    }
}
