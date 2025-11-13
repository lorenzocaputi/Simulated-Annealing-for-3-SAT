# Simulated Annealing as a Solver for the 3-SAT Problem

This repository contains the implementation and analysis of a Simulated Annealing-based solver for the 3-SAT problem, along with comprehensive experimental results investigating algorithmic thresholds and acceptance rate behavior.

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Experimental Results](#experimental-results)
- [File Structure](#file-structure)
- [Research Background](#research-background)
- [References](#references)
- [Author](#author)

## Overview

The K-SAT problem is a fundamental challenge in theoretical computer science and the first problem proven to be NP-complete. This research investigates the performance of **Simulated Annealing** as a solver for 3-SAT instances, with particular focus on:

- **Acceptance rate asymptotic behavior** as problem complexity increases
- **Algorithmic threshold estimation** based on clauses-to-variables ratio (M/N)
- **Limiting algorithmic threshold** discovery at M/N = 4.27

### Problem Formulation

- **Configuration Space**: Boolean assignments to N variables (represented as ±1)
- **Cost Function**: Number of unsatisfied clauses
- **Move Proposal**: Variable sign flipping
- **Optimization**: Metropolis-Hastings algorithm with temperature annealing

## Key Findings

### 1. Acceptance Rate Asymptotic Behavior
- For fixed N, acceptance rate approaches a **lower horizontal asymptote** as M increases
- Asymptotic level decreases with increasing problem complexity (higher M/N ratios)
- Behavior independent of optimization parameter depth

### 2. Algorithmic Threshold Analysis
- **Empirical threshold** found at M/N ratios between **3.5 and 4.2**
- Threshold exhibits **sigmoid-like transition** from solvable to unsolvable regions
- Clear pattern emerges across different problem sizes (N ∈ {200, 300, 400, 500, 600})

### 3. Limiting Algorithmic Threshold
- **Theoretical limit**: M/N = **4.27** (where PSAT = 0.5)
- Better algorithms (more exploration) approach this theoretical limit
- Empirical thresholds: 3.97 → 4.16 with increased MCMC steps

## Technical Architecture

### Core Classes

#### `KSAT` Class (`KSAT.py`)
```python
KSAT(N, M, K, seed=None)
```
- **N**: Number of variables
- **M**: Number of clauses  
- **K**: Literals per clause (=3 for 3-SAT)
- **seed**: Random seed for reproducibility

**Key Methods:**
- `cost()`: Vectorized cost computation (unsatisfied clauses)
- `compute_delta_cost(move)`: Efficient delta cost calculation
- `propose_move()`: Random variable selection for flipping
- `accept_move(move)`: Apply move to current configuration

#### `SimAnn` Module (`SimAnn.py`)
```python
simann(probl, anneal_steps=10, mcmc_steps=100, beta0=0.1, beta1=10.0, ...)
```
- **Temperature Schedule**: Linear (or logarithmic) annealing from β₀ to β₁
- **Early Stopping**: Terminates when solution found (cost = 0)
- **Metropolis Rule**: Probabilistic acceptance based on cost difference

### Optimization Parameters

The research uses carefully chosen fixed parameters:
- **MCMC Steps**: 1000 (move proposals per temperature)
- **Annealing Steps**: 100 (temperature reduction steps)
- **β₀**: 0.1 (initial inverse temperature, ~0.9 acceptance rate)
- **β₁**: 10 (final inverse temperature, ~0.1 acceptance rate)

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

**Dependencies:**
- `numpy` - Numerical computations and vectorization
- `matplotlib` - Plotting and visualization
- `seaborn` - Enhanced statistical plotting

### Quick Start
```bash
git clone <repository-url>
cd lorenzo_caputi_3240499_programming_project
python single_solver.py
```

## Usage

### Single Instance Solving
```python
from KSAT import KSAT
from KSAT_functions import solve, plot_acc_rates

# Create 3-SAT instance
ksat = KSAT(N=200, M=800, K=3, seed=42)

# Solve with Simulated Annealing
best, acc_rates = solve(ksat, mcmc_steps=1000, anneal_steps=100, 
                       beta0=0.1, beta1=10, seed=42)

# Visualize acceptance rate evolution
plot_acc_rates(acc_rates)
```

### Algorithmic Threshold Analysis
```python
from KSAT_functions import solve_multiple_M, plot_multiple_probabilities

# Test multiple clause numbers
N = 200
M_values = [600, 700, 800, 850, 900, 950]

solutions, acc_rates_dict = solve_multiple_M(
    N, M_values, K=3, mcmc_steps=1000, anneal_steps=100,
    beta0=0.1, beta1=10, seed=42, logspace=False, early_stopping=True
)
```

### Available Scripts

| Script | Purpose |
|--------|---------|
| `single_solver.py` | Solve single instance and plot acceptance rates |
| `multiple_solver.py` | Compare acceptance rates across different M values |
| `plot_probability.py` | Estimate solving probability vs. clause number |
| `plot_probabilities_multiple_m.py` | Multi-N threshold analysis |
| `limiting_alg_threshold.py` | Parameter optimization impact study |
| `intersections.py` | Algorithmic threshold calculation |
| `cost_efficiency.py` | Cost function performance comparison |
| `time_efficiency_delta_c.py` | Delta cost computation benchmarking |

## Experimental Results

### Performance Data
The `data.csv` file contains **95+ experimental configurations** testing:
- **Problem sizes**: N ∈ {200, 300, 400, 500, 600, 700}
- **Clause ranges**: M from 600 to 3150
- **Parameter variations**: MCMC steps from 1000 to 20000
- **Success rates**: Empirical solving probabilities

### Key Measurements

#### Algorithmic Thresholds (M/N ratios)
| N | Threshold (M) | Threshold (M/N) |
|---|---------------|-----------------|
| 200 | 795 | 3.97 |
| 300 | 1154 | 3.84 |
| 400 | 1526 | 3.81 |
| 500 | 1822 | 3.64 |
| 600 | 2155 | 3.59 |

#### Parameter Impact on Threshold Estimation
| MCMC Steps | Estimated Threshold (M/N) |
|------------|---------------------------|
| 1000 | 3.97 |
| 2000 | 4.07 |
| 3000 | 4.13 |
| 4000 | 4.15 |
| 5000 | 4.16 |

## File Structure

```
├── article.pdf                          # Complete research paper
├── KSAT.py                             # K-SAT problem class
├── SimAnn.py                           # Simulated Annealing solver
├── KSAT_functions.py                   # Utility functions and plotting
├── requirements.txt                    # Python dependencies
├── data.csv                           # Experimental results data
├── psat.csv                           # Additional probability data
│
├── Analysis Scripts:
├── single_solver.py                   # Single instance analysis
├── multiple_solver.py                 # Multi-instance comparison
├── plot_probability.py                # Probability estimation
├── plot_probabilities_multiple_m.py   # Multi-N analysis
├── limiting_alg_threshold.py          # Parameter impact study
├── intersections.py                   # Threshold calculations
│
├── Performance Analysis:
├── cost_efficiency.py                 # Cost function benchmarking
├── time_efficiency_delta_c.py         # Delta cost optimization
├── multi_plot.py                      # Multi-subplot visualization
└── 3SAT_properties.py                 # Problem property analysis
```

## Research Background

### Theoretical Context
The 3-SAT problem is **NP-complete**, meaning no known polynomial-time algorithm exists for its solution. This research contributes to understanding:

1. **Phase Transitions**: Sharp transitions from satisfiable to unsatisfiable regions
2. **Algorithmic Performance**: How heuristic solvers behave near critical points
3. **Statistical Physics**: Connections between optimization and physical systems

### Related Approaches
- **DPLL Algorithm**: Systematic backtracking approach
- **WalkSAT**: Local search with random restarts
- **Statistical Physics Methods**: Replica symmetry breaking analysis

### Key Contributions
1. **Empirical validation** of theoretical phase transition predictions
2. **Algorithmic threshold characterization** for Simulated Annealing
3. **Performance optimization** through parameter analysis
4. **Limiting behavior identification** approaching theoretical bounds

## References

1. Cook, S. A. "The complexity of theorem-proving procedures." *STOC 1971*
2. Davis, M., Logemann, G., & Loveland, D. "A machine program for theorem-proving." *CACM 1962*
3. Selman, B., Kautz, H. A., & Cohen, B. "Noise strategies for improving local search." *AAAI 1994*
4. Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. "Optimization by simulated annealing." *Science 1983*
5. Metropolis, N., et al. "Equation of state calculations by fast computing machines." *JCP 1953*
6. Dubois, O., Boufkhad, Y., & Mandler, J. "Typical random 3-SAT formulae and the satisfiability threshold." *SODA 2000*

## Author

**Lorenzo Caputi** (Student ID: 3240499)  
*BEMACS Program, 2nd Year*  
*Programming Project - January 15, 2025*

---

## Technical Notes

### Cost Function Optimization
Three implementations provided with performance analysis:
- **Vectorized (fastest)**: `cost()` - ~20% faster than alternatives
- **NumPy Product**: `cost_np_prod()` - Intermediate performance  
- **Loop-based**: `cost_for_loop()` - Reference implementation (slowest)

### Reproducibility
All experiments use **seed=42** for consistent results. Random number generation carefully managed across:
- Problem instance creation
- Initial configuration setup
- Move proposal selection
- Metropolis acceptance decisions

### Computational Complexity
- **Time per move**: O(K × clauses_per_variable) ≈ O(M)
- **Space complexity**: O(N + M×K) for problem representation
- **Total runtime**: O(anneal_steps × mcmc_steps × M)

This implementation provides both research-grade analysis tools and practical SAT solving capabilities, with comprehensive documentation and experimental validation of theoretical predictions.
