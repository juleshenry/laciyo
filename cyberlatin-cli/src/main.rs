use rmp_serde;
use clap::{Parser, Subcommand};
use rand::Rng;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{Read, Write};

#[derive(Serialize, Deserialize, Clone, Debug)]
struct Candidate {
    word: String,
    syllables: u32,
    phonemes: Vec<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
struct Concept {
    id: String,
    grammatical_class: String,
    candidates: Vec<Candidate>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
struct State {
    concepts: HashMap<String, Concept>,
    // Mapping of Concept ID to the index of the chosen Candidate
    choices: HashMap<String, usize>,
    energy_score: u64,
}

impl State {
    fn calculate_energy(&mut self) {
        let mut total_syllables = 0;
        let mut global_phonemes: HashSet<String> = HashSet::new();
        let mut ar_stems: HashSet<String> = HashSet::new();
        let mut er_stems: HashSet<String> = HashSet::new();
        let mut ir_stems: HashSet<String> = HashSet::new();
        let mut grammatical_collisions = 0;

        for (concept_id, choice_idx) in &self.choices {
            let concept = &self.concepts[concept_id];
            let candidate = &concept.candidates[*choice_idx];

            total_syllables += candidate.syllables;
            for p in &candidate.phonemes {
                global_phonemes.insert(p.clone());
            }

            // Simple collision check for stems based on class
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

        // Energy = (1000 * Syllables) + (10 * Phonemes) + (100000 * Collisions)
        self.energy_score = (1000 * total_syllables as u64)
            + (10 * global_phonemes.len() as u64)
            + (100_000 * grammatical_collisions as u64);
    }
}

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Start the Simulated Annealing engine
    Start {
        /// Path to the genesis or current .clatin file
        #[arg(short, long)]
        file: String,
    },
    /// Merge a peer's .clatin file
    Merge {
        /// Path to the peer's .clatin file
        #[arg(short, long)]
        peer_file: String,
    },
}

fn load_state(path: &str) -> State {
    let mut file = File::open(path).expect("Failed to open .clatin file");
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).expect("Failed to read file");
    rmp_serde::from_slice(&buffer).expect("Failed to deserialize state")
}

fn save_state(state: &State, path: &str) {
    let encoded = rmp_serde::to_vec(state).expect("Failed to serialize state");
    let mut file = File::create(path).expect("Failed to create file");
    file.write_all(&encoded).expect("Failed to write to file");
}

fn simulated_annealing(mut state: State) -> State {
    println!("Starting Simulated Annealing. Initial Energy: {}", state.energy_score);
    let mut rng = rand::thread_crate();
    
    // Hyperparameters for Simulated Annealing
    let mut temperature = 10000.0;
    let cooling_rate = 0.9999;
    let min_temperature = 0.1;
    let mut iteration = 0;

    let concept_ids: Vec<String> = state.concepts.keys().cloned().collect();

    if concept_ids.is_empty() {
        println!("No concepts to optimize.");
        return state;
    }

    let mut best_state = state.clone();

    while temperature > min_temperature {
        // Create a neighbor
        let mut new_state = state.clone();
        
        // Pick a random concept to mutate
        let random_concept_idx = rng.gen_range(0..concept_ids.len());
        let concept_id = &concept_ids[random_concept_idx];
        let concept = &new_state.concepts[concept_id];
        
        if concept.candidates.len() > 1 {
            let mut new_choice = rng.gen_range(0..concept.candidates.len());
            // Ensure we actually pick a different candidate if possible
            while new_choice == new_state.choices[concept_id] {
                new_choice = rng.gen_range(0..concept.candidates.len());
            }
            new_state.choices.insert(concept_id.clone(), new_choice);
            new_state.calculate_energy();

            let current_energy = state.energy_score;
            let new_energy = new_state.energy_score;

            // Decide whether to accept the neighbor
            if new_energy < current_energy {
                state = new_state; // Accept strictly better state
                if state.energy_score < best_state.energy_score {
                    best_state = state.clone();
                    println!("Iteration {}: New best energy: {}", iteration, best_state.energy_score);
                }
            } else {
                // Accept worse state with some probability
                let acceptance_probability = ((current_energy as f64 - new_energy as f64) / temperature).exp();
                if rng.gen::<f64>() < acceptance_probability {
                    state = new_state;
                }
            }
        }

        temperature *= cooling_rate;
        iteration += 1;
        
        if iteration % 10000 == 0 {
            println!("Temp: {:.2}, Current Energy: {}", temperature, state.energy_score);
        }
    }

    println!("Finished Simulated Annealing. Best Energy: {}", best_state.energy_score);
    best_state
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Start { file } => {
            println!("Loading genome from {}...", file);
            let state = load_state(file);
            let optimized_state = simulated_annealing(state);
            let out_file = "local_optimal.clatin";
            save_state(&optimized_state, out_file);
            println!("Saved optimized genome to {}", out_file);
        }
        Commands::Merge { peer_file } => {
            println!("Loading local optimal genome...");
            let local_state = load_state("local_optimal.clatin");
            println!("Loading peer genome from {}...", peer_file);
            let peer_state = load_state(peer_file);

            println!("Local Energy: {}", local_state.energy_score);
            println!("Peer Energy: {}", peer_state.energy_score);

            if peer_state.energy_score < local_state.energy_score {
                println!("Peer genome is superior! Adopting as new baseline.");
                save_state(&peer_state, "local_optimal.clatin");
            } else {
                println!("Local genome is superior or equal. Rejecting peer genome.");
            }
        }
    }
}
