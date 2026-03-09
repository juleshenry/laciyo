import argparse
import logging
from typing import Dict, List, Any, Set

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def count_syllables(word: str) -> int:
    """
    Heuristic for syllable counting. 
    In a real implementation, this would use a phonetic dictionary (e.g., CMU dict for IPA).
    """
    vowels = "aeiouyáéíóúàèìòùâêîôûäëïöü"
    count = 0
    prev_is_vowel = False
    for char in word.lower():
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    return max(1, count) # At least 1 syllable

def extract_phonemes(word: str) -> Set[str]:
    """
    Mock function to extract phonemes from a word.
    Would use G2P (Grapheme-to-Phoneme) libraries like `epitran` in production.
    """
    return set(list(word.lower()))

def calculate_phonemic_cost(candidate_phonemes: Set[str], global_inventory: Set[str]) -> int:
    """
    Calculates how many *new* phonemes this candidate introduces to the global inventory.
    Lower cost = better for maintaining a minimal, isolating phoneme set.
    """
    return len(candidate_phonemes - global_inventory)

def distributed_lexicon_worker(concept_id: str, candidates: List[str], current_global_inventory: Set[str]) -> str:
    """
    Simulates a single node's calculation in the distributed architecture.
    Selects the best Cyber-Latin word for a given concept based on the calculus.
    """
    logging.info(f"[Worker] Processing concept {concept_id} with candidates: {candidates}")
    
    # 1. Primary Filter: Minimize syllables
    candidates_with_syllables = [(word, count_syllables(word)) for word in candidates]
    min_syllables = min(candidates_with_syllables, key=lambda x: x[1])[1]
    
    # Keep only the candidates tied for the lowest syllable count
    short_candidates = [word for word, syl in candidates_with_syllables if syl == min_syllables]
    
    if len(short_candidates) == 1:
        return short_candidates[0]
    
    # 2. Secondary Filter: Minimize global phonemic impact (NP-hard when optimized globally across ALL concepts simultaneously)
    # This is where the distributed calculus shines. Nodes evaluate different permutations of the lexicon.
    candidates_with_cost = [
        (word, calculate_phonemic_cost(extract_phonemes(word), current_global_inventory)) 
        for word in short_candidates
    ]
    
    # Choose the one that introduces the fewest new phonemes
    best_candidate = min(candidates_with_cost, key=lambda x: x[1])[0]
    return best_candidate

def simulate_distributed_network(concept_map: Dict[str, List[str]]) -> Dict[str, str]:
    """
    Master node function that distributes the workload to workers and aggregates results.
    """
    global_inventory = set()
    final_lexicon = {}
    
    for concept_id, candidates in concept_map.items():
        # In a real system, this is sent over a network (e.g., Celery, Kafka, or a custom P2P protocol)
        best_word = distributed_lexicon_worker(concept_id, candidates, global_inventory)
        final_lexicon[concept_id] = best_word
        
        # Update global inventory with the new word's phonemes
        global_inventory.update(extract_phonemes(best_word))
        logging.info(f"Selected '{best_word}' for {concept_id}. Global phonemes: {len(global_inventory)}")
        
    return final_lexicon

if __name__ == "__main__":
    # Mock data representing our cognate/translation groups across Romance languages
    mock_concepts = {
        "concept_red": ["rouge", "rojo", "vermelho", "rosso"],
        "concept_cable": ["cabo", "cavo", "câble"],
        "concept_water": ["eau", "agua", "acqua", "água"],
        "concept_fire": ["feu", "fuego", "fuoco", "fogo"]
    }
    
    logging.info("Initializing Cyber-Latin Distributed Calculation Network...")
    lexicon = simulate_distributed_network(mock_concepts)
    
    logging.info("\n=== Final Cyber-Latin Core Lexicon ===")
    for concept, word in lexicon.items():
        logging.info(f"{concept}: {word}")
