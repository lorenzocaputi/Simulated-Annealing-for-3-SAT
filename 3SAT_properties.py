import KSAT
import argparse

import numpy as np

from KSAT_functions import solve

""""
Use this file to compute the empirical probability of solving a random instance
of the K-SAT problem, for every combination of the provided values for N and M.

It uses a parser to extract the values for N and M from the command line.

Example usage: python 3SAT_properties.py --N start, stop, step --M start, stop, step

Here "start, stop, step" is a shortcut to extract an array of equally spaced values from start
to stop both included, with equal spacing equal to step.
If one wishes to keep N fixed and try different values for M, just run the program 
with: --N start, start, 1
"""


# seed
seed = 42

# simAnn parameters
mcmc_steps = 1000
anneal_steps = 100
beta0 = 0.1
beta1 = 10
logspace = False
early_stopping = True

# experiment parameters
K = 3
n_instances = 30


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse N and M (numpy arrays) from the command line. Example usage: python 3SAT_properties.py --N 200,300,100 --M 600,1000,200")
    
    parser.add_argument(
        "--N",
        type=str,
        required=True,
        help="elements of N in the form (start, stop, step)"
    )
    parser.add_argument(
        "--M",
        type=str,
        required=True,
        help="elements of M in the form (start, stop, step)"
    )
    
    args = parser.parse_args()

    try:
        N_start, N_stop, N_step = [int(x) for x in args.N.split(",")]
        M_start, M_stop, M_step = [int(x) for x in args.M.split(",")]
    except ValueError:
        raise ValueError("Input must be in the format 'start,stop,step' for both --N and --M.")
    
    N = [int(x) for x in np.arange(N_start, N_stop + N_step, N_step)]
    M = [int(x) for x in np.arange(M_start, M_stop + M_step, M_step)]
    
    return N, M


N, M = parse_arguments()



def solving_probability(N:list, M:list, K:int, n_instances:int):
    P = dict()
    for n in N:
        for m in M:
            solved = 0
            for _ in range(n_instances):
                ksat = KSAT.KSAT(n, m, K, seed=None)
                print(f"\nsolving {K}-SAT with {n} variables and {m} clauses:\n")
                best, _ = solve(ksat, mcmc_steps, anneal_steps, beta0, beta1, seed, logspace, early_stopping)
                if best.cost() == 0:
                    solved += 1
            P[(n, m)] = solved / n_instances
    
    return P


P = solving_probability(N, M, K, n_instances)

print("\n")
for (n, m) in P:
    print(f"Empirical probability of solving {K}-SAT with {n} variables and {m} clauses: {P[(n,m)]}\n")

