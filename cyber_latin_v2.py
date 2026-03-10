#!/usr/bin/env python3
"""
Cyber-Latin v2.0: Hybrid Optimization System

Implements dual-mode lexicon optimization:
- LOCAL mode: Minimize syllables for morpheme-free core vocabulary (rouge, agua, etc.)
- GLOBAL mode: Minimize morpheme inventory for Latin-derived words (transport, information, etc.)

Architecture:
1. Classify all concepts as LOCAL or GLOBAL using morpheme detector
2. For LOCAL concepts: Select candidates that minimize syllable count
3. For GLOBAL concepts: Select candidates that maximize morpheme reuse
4. Combined energy function weights both modes appropriately

Energy Formula:
  E_total = E_local + E_global + E_collision
  
  E_local = 1000 * Σ(syllables) + 10 * Σ(new_phonemes)
  E_global = 500 * Σ(morpheme_syllables) + 100 * |morpheme_inventory| + 5 * Σ(morpheme_phonemes)
  E_collision = 100,000 * grammatical_collisions
"""

import argparse
import logging
import json
from typing import Dict, List, Set, Tuple
from morpheme_detector import MorphemeDetector

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def count_syllables(word: str) -> int:
    """
    Heuristic syllable counting.
    In production, use phonetic dictionary (CMU dict) or epitran.
    """
    vowels = "aeiouyáéíóúàèìòùâêîôûäëïöü"
    count = 0
    prev_is_vowel = False
    for char in word.lower():
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    return max(1, count)


def extract_phonemes(word: str) -> Set[str]:
    """
    Mock phoneme extraction.
    In production, use G2P (epitran, phonemizer, etc.).
    """
    return set(list(word.lower()))


def count_morpheme_syllables(morpheme_inventory: Set[str], morpheme_db: Dict) -> int:
    """
    Calculate total syllables in morpheme inventory.
    Uses morpheme canonical forms (strip hyphens).
    """
    total = 0
    for morpheme in morpheme_inventory:
        # Strip hyphens for syllable counting
        clean_form = morpheme.strip('-')
        total += count_syllables(clean_form)
    return total


def extract_morphemes_from_word(word: str, language: str, detector: MorphemeDetector) -> Set[str]:
    """
    Extract canonical morpheme forms from a word.
    Returns set of morphemes like {"trans-", "-tion"}
    """
    detection = detector.detect_morphemes(word, language)
    morphemes = set()
    morphemes.update(detection["prefixes"])
    morphemes.update(detection["suffixes"])
    return morphemes


def calculate_energy_v2(
    lexicon: Dict[str, str],
    concept_classifications: Dict[str, str],
    concept_languages: Dict[str, str],
    global_phoneme_inventory: Set[str],
    morpheme_inventory: Set[str],
    detector: MorphemeDetector
) -> Tuple[int, Dict]:
    """
    Dual-mode energy calculation.
    
    Args:
        lexicon: Concept ID -> selected word
        concept_classifications: Concept ID -> "LOCAL" or "GLOBAL"
        concept_languages: Concept ID -> language code (for morpheme detection)
        global_phoneme_inventory: Set of phonemes used across entire lexicon
        morpheme_inventory: Set of canonical morphemes used (e.g., {"trans-", "-tion"})
        detector: MorphemeDetector instance
    
    Returns:
        (total_energy, energy_breakdown)
    """
    energy_breakdown = {
        "local_syllables": 0,
        "local_phonemes": 0,
        "global_morpheme_syllables": 0,
        "global_morpheme_inventory_size": 0,
        "global_morpheme_phonemes": 0,
        "grammatical_collisions": 0,
        "total": 0
    }
    
    # === LOCAL ENERGY ===
    # Minimize syllables and phonemes for morpheme-free words
    local_concepts = [cid for cid, cls in concept_classifications.items() if cls == "LOCAL"]
    
    local_syllable_count = 0
    for concept_id in local_concepts:
        if concept_id in lexicon:
            word = lexicon[concept_id]
            local_syllable_count += count_syllables(word)
    
    energy_breakdown["local_syllables"] = local_syllable_count
    local_syllable_energy = 1000 * local_syllable_count
    
    # Phoneme diversity cost (encourage minimal phoneme inventory)
    local_phoneme_energy = 10 * len(global_phoneme_inventory)
    energy_breakdown["local_phonemes"] = len(global_phoneme_inventory)
    
    # === GLOBAL ENERGY ===
    # Minimize morpheme inventory size for morpheme-bearing words
    global_concepts = [cid for cid, cls in concept_classifications.items() if cls == "GLOBAL"]
    
    morpheme_syllable_count = count_morpheme_syllables(morpheme_inventory, detector.morpheme_db)
    energy_breakdown["global_morpheme_syllables"] = morpheme_syllable_count
    global_morpheme_syllable_energy = 500 * morpheme_syllable_count  # Lower weight than local
    
    # Penalize large morpheme inventories (encourage reuse)
    morpheme_inventory_size = len(morpheme_inventory)
    energy_breakdown["global_morpheme_inventory_size"] = morpheme_inventory_size
    global_inventory_energy = 100 * morpheme_inventory_size
    
    # Morpheme phoneme diversity
    morpheme_phonemes = set()
    for morpheme in morpheme_inventory:
        clean_form = morpheme.strip('-')
        morpheme_phonemes.update(extract_phonemes(clean_form))
    
    energy_breakdown["global_morpheme_phonemes"] = len(morpheme_phonemes)
    global_phoneme_energy = 5 * len(morpheme_phonemes)
    
    # === UNIVERSAL PENALTY ===
    # Grammatical collisions (homonyms) are heavily penalized
    word_counts = {}
    for word in lexicon.values():
        word_counts[word] = word_counts.get(word, 0) + 1
    
    collision_count = sum(1 for count in word_counts.values() if count > 1)
    energy_breakdown["grammatical_collisions"] = collision_count
    collision_energy = 100_000 * collision_count
    
    # === TOTAL ENERGY ===
    total_energy = (
        local_syllable_energy +
        local_phoneme_energy +
        global_morpheme_syllable_energy +
        global_inventory_energy +
        global_phoneme_energy +
        collision_energy
    )
    
    energy_breakdown["total"] = total_energy
    
    return total_energy, energy_breakdown


def optimize_lexicon_v2(
    concept_map: Dict[str, Dict[str, str]],
    detector: MorphemeDetector
) -> Dict[str, any]:
    """
    Main optimization function using dual-mode energy calculation.
    
    Args:
        concept_map: {
            "concept_id": {
                "fr": "word_fr",
                "es": "word_es",
                "it": "word_it",
                "pt": "word_pt"
            }
        }
    
    Returns:
        {
            "lexicon": {"concept_id": "selected_word"},
            "classifications": {"concept_id": "LOCAL|GLOBAL"},
            "morpheme_inventory": ["trans-", "-tion", ...],
            "energy": total_energy,
            "energy_breakdown": {...}
        }
    """
    logging.info("=" * 70)
    logging.info("CYBER-LATIN v2.0: HYBRID OPTIMIZATION")
    logging.info("=" * 70)
    
    # === PHASE 1: CLASSIFY ALL CONCEPTS ===
    logging.info("\n[PHASE 1] Classifying concepts as LOCAL or GLOBAL...")
    
    concept_classifications = {}
    for concept_id, candidates in concept_map.items():
        classification = detector.classify_concept(candidates)
        concept_classifications[concept_id] = classification
        logging.info(f"  {concept_id}: {classification}")
    
    local_count = sum(1 for c in concept_classifications.values() if c == "LOCAL")
    global_count = sum(1 for c in concept_classifications.values() if c == "GLOBAL")
    logging.info(f"\nClassification Summary: {local_count} LOCAL, {global_count} GLOBAL")
    
    # === PHASE 2: OPTIMIZE LOCAL CONCEPTS ===
    logging.info("\n[PHASE 2] Optimizing LOCAL concepts (syllable minimization)...")
    
    lexicon = {}
    concept_languages = {}
    global_phoneme_inventory = set()
    
    local_concepts = [cid for cid, cls in concept_classifications.items() if cls == "LOCAL"]
    
    for concept_id in local_concepts:
        candidates = concept_map[concept_id]
        
        # Find candidate with minimum syllables
        candidates_with_syllables = [(lang, word, count_syllables(word)) 
                                     for lang, word in candidates.items()]
        best_lang, best_word, min_syllables = min(candidates_with_syllables, key=lambda x: x[2])
        
        lexicon[concept_id] = best_word
        concept_languages[concept_id] = best_lang
        global_phoneme_inventory.update(extract_phonemes(best_word))
        
        logging.info(f"  {concept_id}: {best_word} ({best_lang}, {min_syllables} syllables)")
    
    # === PHASE 3: OPTIMIZE GLOBAL CONCEPTS ===
    logging.info("\n[PHASE 3] Optimizing GLOBAL concepts (morpheme reuse)...")
    
    morpheme_inventory = set()
    global_concepts = [cid for cid, cls in concept_classifications.items() if cls == "GLOBAL"]
    
    # Simple greedy strategy: pick candidate that introduces fewest new morphemes
    for concept_id in global_concepts:
        candidates = concept_map[concept_id]
        
        best_candidate = None
        best_lang = None
        min_new_morphemes = float('inf')
        
        for lang, word in candidates.items():
            # Extract morphemes from this candidate
            word_morphemes = extract_morphemes_from_word(word, lang, detector)
            
            # Count how many are new (not in inventory yet)
            new_morphemes = word_morphemes - morpheme_inventory
            new_count = len(new_morphemes)
            
            if new_count < min_new_morphemes:
                min_new_morphemes = new_count
                best_candidate = word
                best_lang = lang
                best_morphemes = word_morphemes
        
        lexicon[concept_id] = best_candidate
        concept_languages[concept_id] = best_lang
        morpheme_inventory.update(best_morphemes)
        global_phoneme_inventory.update(extract_phonemes(best_candidate))
        
        logging.info(f"  {concept_id}: {best_candidate} ({best_lang}, morphemes: {best_morphemes})")
    
    # === PHASE 4: CALCULATE FINAL ENERGY ===
    logging.info("\n[PHASE 4] Calculating total energy...")
    
    total_energy, energy_breakdown = calculate_energy_v2(
        lexicon,
        concept_classifications,
        concept_languages,
        global_phoneme_inventory,
        morpheme_inventory,
        detector
    )
    
    logging.info(f"\nEnergy Breakdown:")
    logging.info(f"  LOCAL syllables: {energy_breakdown['local_syllables']} x 1000 = {1000 * energy_breakdown['local_syllables']}")
    logging.info(f"  LOCAL phonemes: {energy_breakdown['local_phonemes']} x 10 = {10 * energy_breakdown['local_phonemes']}")
    logging.info(f"  GLOBAL morpheme syllables: {energy_breakdown['global_morpheme_syllables']} x 500 = {500 * energy_breakdown['global_morpheme_syllables']}")
    logging.info(f"  GLOBAL inventory size: {energy_breakdown['global_morpheme_inventory_size']} x 100 = {100 * energy_breakdown['global_morpheme_inventory_size']}")
    logging.info(f"  GLOBAL morpheme phonemes: {energy_breakdown['global_morpheme_phonemes']} x 5 = {5 * energy_breakdown['global_morpheme_phonemes']}")
    logging.info(f"  Grammatical collisions: {energy_breakdown['grammatical_collisions']} x 100,000 = {100_000 * energy_breakdown['grammatical_collisions']}")
    logging.info(f"  TOTAL ENERGY: {total_energy}")
    
    # === RETURN RESULTS ===
    return {
        "lexicon": lexicon,
        "classifications": concept_classifications,
        "morpheme_inventory": sorted(list(morpheme_inventory)),
        "global_phonemes": sorted(list(global_phoneme_inventory)),
        "energy": total_energy,
        "energy_breakdown": energy_breakdown
    }


def main():
    """CLI interface for testing the v2 optimizer."""
    parser = argparse.ArgumentParser(description="Cyber-Latin v2.0 Hybrid Optimizer")
    parser.add_argument('--concepts', default='data/test_concepts.json',
                       help='Path to concept map JSON file')
    parser.add_argument('--output', default='results_v2.json',
                       help='Output file for optimization results')
    args = parser.parse_args()
    
    # Load concept map
    with open(args.concepts, 'r', encoding='utf-8') as f:
        data = json.load(f)
        concept_map = {cid: cdata['candidates'] for cid, cdata in data['concepts'].items()}
    
    # Initialize detector
    detector = MorphemeDetector()
    
    # Run optimization
    results = optimize_lexicon_v2(concept_map, detector)
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logging.info(f"\n{'='*70}")
    logging.info(f"Results saved to {args.output}")
    logging.info(f"{'='*70}")
    
    # Print final lexicon
    logging.info("\n=== FINAL CYBER-LATIN LEXICON ===")
    for concept_id, word in sorted(results['lexicon'].items()):
        classification = results['classifications'][concept_id]
        logging.info(f"  {concept_id:25s} -> {word:20s} [{classification}]")
    
    logging.info(f"\n=== MORPHEME INVENTORY ({len(results['morpheme_inventory'])} morphemes) ===")
    logging.info(f"  {', '.join(results['morpheme_inventory'])}")


if __name__ == "__main__":
    main()
