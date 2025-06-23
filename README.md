# Cairo Roller - Provably Fair Dice Rolling

A Cairo executable application implementing provably fair dice rolling using continuous hash chains. This system provides production-ready functionality for integration into gaming systems with complete transparency and verifiability.

## 🎯 Purpose

Cairo Roller provides:
- **Provably Fair Dice Rolling**: Each roll can be independently verified
- **Hash Chain Continuity**: Rolls build upon previous results, creating an unbroken chain
- **Production Ready**: Core functions ready for integration into applications
- **Statistical Analysis**: Built-in tools to verify randomness distribution

## 🔐 How It Works

### Hash Chain System
1. **Start with a seed**: Initial random value (kept secret until reveal)
2. **Generate commitment**: `commitment = hash(seed, 0)` (published before rolling)
3. **Create continuous chain**: Each roll generates the next hash using the previous result
   ```
   hash₁ = hash(seed, 1)         → dice_roll₁
   hash₂ = hash(hash₁, 1)        → dice_roll₂
   hash₃ = hash(hash₂, 1)        → dice_roll₃
   ...
   ```

### Provably Fair Process
1. **Commit Phase**: Publisher commits to a seed (publishes hash, keeps seed secret)
2. **Roll Phase**: Dice are rolled using the hash chain
3. **Reveal Phase**: Seed is revealed, allowing full verification
4. **Verify Phase**: Anyone can independently verify all rolls

## 🚀 Quick Start

### Prerequisites
- [Scarb](https://docs.swmansion.com/scarb/) (Cairo package manager)
- Python 3.x for distribution analysis

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd cairoroller

# Build the project
scarb build
```

### Basic Usage
```bash
# Run dice roller with 10 dice
scarb execute --arguments 10

# Analyze distribution of results
scarb execute --arguments 1000 | python3 analyze_distribution.py
```

## 📊 Proving and Verifying Rolls

### For Game Publishers

1. **Generate commitment before game starts:**
```bash
# The commitment is automatically generated and displayed
scarb execute --arguments 5
# Output shows: "Commitment (published before rolling): 0x..."
```

2. **Publish the commitment hash** to players before rolling

3. **Reveal the seed after rolling** to allow verification

### For Players/Verifiers

1. **Verify the commitment:**
   - Check that `hash(revealed_seed, 0) == published_commitment`

2. **Verify the roll sequence:**
   - Recreate the hash chain using the revealed seed
   - Confirm each roll matches the expected hash result

3. **Independent verification:**
```bash
# Use the revealed seed to verify results
scarb execute --arguments <num_dice>  # Should produce identical results
```

### Hash Chain Verification Process

Given a revealed seed, you can verify the entire chain:

```cairo
// Pseudo-code for verification
fn verify_rolls(seed: felt252, expected_rolls: Array<u8>) -> bool {
    let mut current_hash = seed;
    
    for (i, expected_roll) in expected_rolls.iter().enumerate() {
        current_hash = get_next_hash_value(current_hash);
        let actual_roll = hash_to_dice_roll(current_hash);
        
        if actual_roll != expected_roll {
            return false;
        }
    }
    
    true
}
```

## 📈 Analyzing Roll Distribution

The included Python script provides comprehensive statistical analysis:

### Statistical Tests Performed
- **Chi-square test**: Tests if distribution deviates significantly from fair (α = 0.05)
- **Frequency analysis**: Counts and percentages for each face (1-6)
- **Range analysis**: Distribution across low (1-2), mid (3-4), high (5-6) ranges
- **Pattern analysis**: Consecutive same numbers and other patterns

### Usage Examples

```bash
# Analyze 1000 rolls
scarb execute --arguments 1000 | python3 analyze_distribution.py

# Test with different sample sizes
scarb execute --arguments 100 | python3 analyze_distribution.py
scarb execute --arguments 10000 | python3 analyze_distribution.py
```

### Interpreting Results

The analysis provides:
- **✅ Fair distribution**: Chi-square < 11.070 (5% significance level)
- **⚠️ Potentially unfair**: Chi-square ≥ 11.070 (requires investigation)
- **Expected values**: Mean ≈ 3.5, Standard deviation ≈ 1.708

Example output:
```
=== DICE ROLL DISTRIBUTION ANALYSIS ===
Total rolls: 1000

FREQUENCY ANALYSIS:
Face | Count | Percentage | Expected | Deviation
--------------------------------------------------
  1  |  167  |   16.7%   |  166.7  |   +0.3
  2  |  165  |   16.5%   |  166.7  |   -1.7
  ...

Chi-square statistic: 2.456
Critical value (5% significance, 5 df): 11.070
✅ Distribution appears fair (fails to reject null hypothesis)
```

## 🔧 Development

### Project Structure
```
cairoroller/
├── src/
│   └── lib.cairo          # Main dice rolling implementation
├── tests/
│   └── test_contract.cairo # Unit tests
├── analyze_distribution.py # Statistical analysis tool
├── Scarb.toml             # Project configuration
└── README.md              # This file
```

### Running Tests
```bash
# Run all tests
scarb test

# Run with coverage (if configured)
scarb test --coverage
```

### Key Functions

- `roll_dice_chain(starting_hash, num_dice)`: Core rolling function
- `start_dice_chain(seed, num_dice)`: Begin a new chain
- `continue_dice_chain(previous_hash, num_dice)`: Continue existing chain
- `generate_commitment(seed)`: Create commitment hash

## 🎓 Integration & Usage

### Provably Fair Implementation

This executable provides production-ready implementations of provably fair concepts:

```cairo
// Core pattern for integration
let commitment = generate_commitment(secret_seed);
// Publish commitment before rolling

// Execute rolls
let (results, final_hash) = start_dice_chain(secret_seed, num_dice);
// Store final_hash for chain continuation

// Continue chain in subsequent operations
let (more_results, new_hash) = continue_dice_chain(final_hash, more_dice);
```

### Key Concepts & Features
- **Commitment schemes**: Pre-committing to randomness sources
- **Hash chain integrity**: Each result builds on the previous
- **Deterministic verification**: Same inputs always produce same outputs
- **Statistical analysis**: Tools to verify distribution fairness
- **Modular design**: Functions can be integrated into larger systems

## 🛡️ Security Considerations

1. **Seed Security**: Keep seeds secret until reveal phase
2. **Commitment Timing**: Publish commitments before any game actions
3. **Hash Chain Integrity**: Ensure continuous chain without gaps
4. **Reveal Timing**: Reveal seeds promptly after rolling

## 📚 Technical Details

- **Hash Function**: Pedersen hash (Cairo native)
- **Distribution**: Modulo 6 + 1 for uniform distribution
- **Chain Structure**: Each hash depends on the previous result
- **Execution**: Standalone Cairo executable application

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests for new functionality
4. Run statistical analysis on test results
5. Submit a pull request

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the [LICENSE](LICENSE) file for details.

### Commercial Licensing

**Commercial licenses are available for organizations that wish to use this software in proprietary applications without the AGPL-3.0 copyleft requirements.**

For commercial licensing inquiries, please contact:
- Email: [hi (at) ztb dot dev]
- Website: [https://ztb.dev]

Commercial licenses include:
- Freedom to use in proprietary software
- No requirement to open source your application
- Priority support and maintenance
- Custom development services available


---

*Production-ready provably fair dice rolling in Cairo* 