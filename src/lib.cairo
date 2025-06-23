// Hash-based Provably Fair Dice Roller using Continuous Hash Chains
// Copyright (C) 2025 [Zachary Blake]
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

use core::pedersen::pedersen;

/// Generates the next hash value in the chain from the previous hash
/// This is the core of the hash chain continuation
fn get_next_hash_value(previous_hash: felt252) -> felt252 {
    pedersen(previous_hash, 1)
}

/// Converts a hash value to a dice roll in range [1, 6]
/// Uses modulo operation to ensure uniform distribution
fn hash_to_dice_roll(hash_value: felt252) -> u8 {
    let hash_u256: u256 = hash_value.into();
    let roll_value = (hash_u256 % 6) + 1;
    roll_value.try_into().unwrap()
}

/// Generates a commitment hash for the initial seed
/// Used in commit-reveal schemes for provably fair gaming
fn generate_commitment(seed: felt252) -> felt252 {
    pedersen(seed, 0)
}

/// Rolls multiple dice using continuous hash chain
/// Each roll uses the hash from the previous roll, creating an unbroken chain
/// Returns both the dice results and the final hash for chain continuation
fn roll_dice_chain(starting_hash: felt252, num_dice: u32) -> (Array<u8>, felt252) {
    assert(num_dice > 0, 'Number of dice must be positive');

    let mut results = ArrayTrait::new();
    let mut current_hash = starting_hash;
    let mut i: u32 = 0;

    while i != num_dice {
        current_hash = get_next_hash_value(current_hash);
        let roll = hash_to_dice_roll(current_hash);
        results.append(roll);
        i += 1;
    }

    (results, current_hash)
}

/// Convenience function to start a new hash chain from a seed
/// Returns both results and the final hash for continuing the chain
fn start_dice_chain(seed: felt252, num_dice: u32) -> (Array<u8>, felt252) {
    roll_dice_chain(seed, num_dice)
}

/// Continue rolling dice from where a previous chain left off
/// This is the same as roll_dice_chain but with a more descriptive name
fn continue_dice_chain(previous_hash: felt252, num_dice: u32) -> (Array<u8>, felt252) {
    roll_dice_chain(previous_hash, num_dice)
}

/// Main executable function for the dice roller
/// Demonstrates the continuous hash chain approach
/// If hash_checkpoint is 0, starts a new chain with the seed
/// If hash_checkpoint is non-zero, continues from that checkpoint
#[executable]
fn main(seed: felt252, num_dice: u32, hash_checkpoint: felt252) -> Array<u8> {
    let commitment = generate_commitment(seed);

    println!("=== Continuous Hash Chain Dice Rolling ===");
    println!("Rolling {} dice", num_dice);
    println!("Commitment (published before rolling): {}", commitment);
    println!("Seed (revealed after rolling): {}", seed);

    // Start the hash chain or continue from checkpoint
    let (results, final_hash) = if hash_checkpoint == 0 {
        start_dice_chain(seed, num_dice)
    } else {
        println!("Continuing from hash checkpoint: {}", hash_checkpoint);
        continue_dice_chain(hash_checkpoint, num_dice)
    };
    println!("Results: {:?}", results);
    println!("Final hash (for chain continuation): {}", final_hash);

    // Demonstrate chain continuation
    println!("\n=== Chain Continuation Demo ===");
    let (more_results, next_hash) = continue_dice_chain(final_hash, 3);
    println!("Continued with 3 more rolls: {:?}", more_results);
    println!("New final hash: {}", next_hash);

    results
}
