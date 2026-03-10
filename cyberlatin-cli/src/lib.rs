use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Candidate {
    pub word: String,
    pub syllables: u32,
    pub phonemes: Vec<String>,
    #[serde(default)]
    pub language: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Concept {
    pub id: String,
    pub grammatical_class: String,
    pub candidates: Vec<Candidate>,
    #[serde(default)]
    pub classification: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct State {
    pub concepts: HashMap<String, Concept>,
    pub choices: HashMap<String, usize>,
    pub energy_score: u64,
    #[serde(default)]
    pub morpheme_inventory: HashSet<String>,
}

// Helper functions for morpheme detection
pub fn count_syllables(word: &str) -> u32 {
    let vowels = "aeiouyáéíóúàèìòùâêîôûäëïöü";
    let mut count = 0;
    let mut prev_is_vowel = false;
    
    for c in word.to_lowercase().chars() {
        let is_vowel = vowels.contains(c);
        if is_vowel && !prev_is_vowel {
            count += 1;
        }
        prev_is_vowel = is_vowel;
    }
    
    count.max(1)
}

pub fn extract_phonemes(word: &str) -> HashSet<String> {
    word.to_lowercase()
        .chars()
        .map(|c| c.to_string())
        .collect()
}

pub fn extract_morphemes_simple(word: &str) -> HashSet<String> {
    let prefixes = vec![
        "trans-", "inter-", "sub-", "super-", "in-", "ex-", "con-", "de-", "re-",
        "pre-", "post-", "anti-", "pro-", "ad-", "ab-"
    ];
    
    let suffixes = vec![
        "-tion", "-ation", "-sion", "-ment", "-ness", "-ity", "-ty", "-er", "-or",
        "-al", "-ial", "-ous", "-ious", "-ive", "-able", "-ible", "-ure", "-ant", "-ent"
    ];
    
    let mut detected = HashSet::new();
    let word_lower = word.to_lowercase();
    
    for prefix in &prefixes {
        let prefix_clean = prefix.trim_end_matches('-');
        if word_lower.starts_with(prefix_clean) && word_lower.len() > prefix_clean.len() + 2 {
            detected.insert(prefix.to_string());
        }
    }
    
    for suffix in &suffixes {
        let suffix_clean = suffix.trim_start_matches('-');
        if word_lower.ends_with(suffix_clean) && word_lower.len() > suffix_clean.len() + 2 {
            detected.insert(suffix.to_string());
        }
    }
    
    detected
}

impl State {
    pub fn calculate_energy(&mut self) {
        let mut local_syllables = 0;
        let mut global_phonemes: HashSet<String> = HashSet::new();
        let mut ar_stems: HashSet<String> = HashSet::new();
        let mut er_stems: HashSet<String> = HashSet::new();
        let mut ir_stems: HashSet<String> = HashSet::new();
        let mut grammatical_collisions = 0;
        
        let mut morpheme_inventory = HashSet::new();
        let mut morpheme_syllables = 0;

        for (concept_id, choice_idx) in &self.choices {
            let concept = &self.concepts[concept_id];
            let candidate = &concept.candidates[*choice_idx];
            
            for p in &candidate.phonemes {
                global_phonemes.insert(p.clone());
            }

            if concept.classification == "LOCAL" {
                local_syllables += candidate.syllables;
            } else if concept.classification == "GLOBAL" {
                let morphemes = extract_morphemes_simple(&candidate.word);
                for morpheme in morphemes {
                    morpheme_inventory.insert(morpheme.clone());
                }
            }

            if concept.grammatical_class == "verb-ar" {
                if !ar_stems.insert(candidate.word.clone()) {
                    grammatical_collisions += 1;
                }
            } else if concept.grammatical_class == "verb-er" {
                if !er_stems.insert(candidate.word.clone()) {
                    grammatical_collisions += 1;
                }
            } else if concept.grammatical_class == "verb-ir" {
                if !ir_stems.insert(candidate.word.clone()) {
                    grammatical_collisions += 1;
                }
            }
        }
        
        for morpheme in &morpheme_inventory {
            let clean = morpheme.trim_matches('-');
            morpheme_syllables += count_syllables(clean);
        }
        
        let mut morpheme_phonemes = HashSet::new();
        for morpheme in &morpheme_inventory {
            let clean = morpheme.trim_matches('-');
            morpheme_phonemes.extend(extract_phonemes(clean));
        }
        
        self.morpheme_inventory = morpheme_inventory.clone();

        let local_energy = (1000 * local_syllables as u64) 
            + (10 * global_phonemes.len() as u64);
        
        let global_energy = (500 * morpheme_syllables as u64)
            + (100 * morpheme_inventory.len() as u64)
            + (5 * morpheme_phonemes.len() as u64);
        
        let collision_energy = 100_000 * grammatical_collisions as u64;
        
        self.energy_score = local_energy + global_energy + collision_energy;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_syllables() {
        // Note: These counts are based on our heuristic, not phonetic reality
        // The heuristic counts written vowel sequences, not phonemes
        assert_eq!(count_syllables("rouge"), 2); // o-u-e has consonant 'g' between, so 2 sequences
        assert_eq!(count_syllables("agua"), 2);  // a-u-a has consonant 'g' between, so 2 sequences  
        assert_eq!(count_syllables("transport"), 2); // a-o = 2 sequences
        assert_eq!(count_syllables("information"), 4); // i-o-a-io = 4 sequences
        assert_eq!(count_syllables("international"), 5); // i-e-a-io-a = 5 sequences
        assert_eq!(count_syllables("soleil"), 2); // o-ei has consonant 'l' between, so 2 sequences
        assert_eq!(count_syllables("eau"), 1); // e-au is one continuous vowel sequence
    }

    #[test]
    fn test_extract_phonemes() {
        let phonemes = extract_phonemes("rouge");
        assert_eq!(phonemes.len(), 5);
        assert!(phonemes.contains(&"r".to_string()));
        assert!(phonemes.contains(&"o".to_string()));
        
        let phonemes2 = extract_phonemes("aa");
        assert_eq!(phonemes2.len(), 1);
    }

    #[test]
    fn test_extract_morphemes_global_words() {
        let morphemes1 = extract_morphemes_simple("transport");
        assert!(morphemes1.contains("trans-"), "Should detect 'trans-' prefix");
        
        let morphemes2 = extract_morphemes_simple("information");
        assert!(morphemes2.contains("-tion"), "Should detect '-tion' suffix");
        
        let morphemes3 = extract_morphemes_simple("international");
        assert!(morphemes3.contains("inter-"), "Should detect 'inter-' prefix");
        assert!(morphemes3.contains("-al"), "Should detect '-al' suffix");
        
        let morphemes4 = extract_morphemes_simple("subversion");
        assert!(morphemes4.contains("sub-"), "Should detect 'sub-' prefix");
        assert!(morphemes4.contains("-sion"), "Should detect '-sion' suffix");
    }

    #[test]
    fn test_extract_morphemes_local_words() {
        let morphemes1 = extract_morphemes_simple("rouge");
        assert!(morphemes1.is_empty(), "Rouge should have no morphemes");
        
        let morphemes2 = extract_morphemes_simple("agua");
        assert!(morphemes2.is_empty(), "Agua should have no morphemes");
        
        let morphemes3 = extract_morphemes_simple("soleil");
        assert!(morphemes3.is_empty(), "Soleil should have no morphemes");
        
        let morphemes4 = extract_morphemes_simple("sol");
        assert!(morphemes4.is_empty(), "Sol should have no morphemes (root too short)");
    }

    #[test]
    fn test_energy_calculation_local_concept() {
        let mut concepts = HashMap::new();
        let mut choices = HashMap::new();
        
        let concept = Concept {
            id: "concept_red".to_string(),
            grammatical_class: "adjective".to_string(),
            classification: "LOCAL".to_string(),
            candidates: vec![
                Candidate {
                    word: "rouge".to_string(),
                    syllables: 1,
                    phonemes: vec!["r".to_string(), "o".to_string(), "u".to_string(), "g".to_string(), "e".to_string()],
                    language: "fr".to_string(),
                },
            ],
        };
        
        concepts.insert("concept_red".to_string(), concept);
        choices.insert("concept_red".to_string(), 0);
        
        let mut state = State {
            concepts,
            choices,
            energy_score: 0,
            morpheme_inventory: HashSet::new(),
        };
        
        state.calculate_energy();
        assert_eq!(state.energy_score, 1050, "Energy should be 1000*1 + 10*5 = 1050");
    }

    #[test]
    fn test_energy_calculation_global_concept() {
        let mut concepts = HashMap::new();
        let mut choices = HashMap::new();
        
        let concept = Concept {
            id: "concept_transport".to_string(),
            grammatical_class: "noun".to_string(),
            classification: "GLOBAL".to_string(),
            candidates: vec![
                Candidate {
                    word: "transport".to_string(),
                    syllables: 2,
                    phonemes: vec!["t".to_string(), "r".to_string(), "a".to_string(), "n".to_string(), "s".to_string(), "p".to_string(), "o".to_string()],
                    language: "en".to_string(),
                },
            ],
        };
        
        concepts.insert("concept_transport".to_string(), concept);
        choices.insert("concept_transport".to_string(), 0);
        
        let mut state = State {
            concepts,
            choices,
            energy_score: 0,
            morpheme_inventory: HashSet::new(),
        };
        
        state.calculate_energy();
        
        assert!(state.morpheme_inventory.contains("trans-"), "Should contain 'trans-' morpheme");
        assert!(state.energy_score > 500, "Energy should include GLOBAL costs");
        assert!(state.energy_score < 1000, "Energy should be less than pure LOCAL cost");
    }

    #[test]
    fn test_grammatical_collision_detection() {
        let mut concepts = HashMap::new();
        let mut choices = HashMap::new();
        
        let verb1 = Concept {
            id: "concept_walk".to_string(),
            grammatical_class: "verb-ar".to_string(),
            classification: "LOCAL".to_string(),
            candidates: vec![
                Candidate {
                    word: "andar".to_string(),
                    syllables: 2,
                    phonemes: vec!["a".to_string(), "n".to_string(), "d".to_string(), "r".to_string()],
                    language: "es".to_string(),
                },
            ],
        };
        
        let verb2 = Concept {
            id: "concept_dance".to_string(),
            grammatical_class: "verb-ar".to_string(),
            classification: "LOCAL".to_string(),
            candidates: vec![
                Candidate {
                    word: "andar".to_string(),
                    syllables: 2,
                    phonemes: vec!["a".to_string(), "n".to_string(), "d".to_string(), "r".to_string()],
                    language: "es".to_string(),
                },
            ],
        };
        
        concepts.insert("concept_walk".to_string(), verb1);
        concepts.insert("concept_dance".to_string(), verb2);
        choices.insert("concept_walk".to_string(), 0);
        choices.insert("concept_dance".to_string(), 0);
        
        let mut state = State {
            concepts,
            choices,
            energy_score: 0,
            morpheme_inventory: HashSet::new(),
        };
        
        state.calculate_energy();
        assert!(state.energy_score >= 100_000, "Should have collision penalty");
    }
}
