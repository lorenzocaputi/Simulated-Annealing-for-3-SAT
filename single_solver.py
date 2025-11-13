import KSAT

from KSAT_functions import solve, plot_acc_rates

"""
Use this file to solve a single instance of the K-SAT problem
and plot the evolution of the acceptance rate
"""

seed = 42

# problem variables
N = 200
M = 200
K = 3

# optimization parameters
mcmc_steps = 1000
anneal_steps = 100
beta0 = 0.1
beta1 = 10
logspace = False        # if set to True, the betas in the annealing schedule are logarithmically spaced (log10)
early_stopping = False  # this stops the optimization as soon as a solution is found


ksat = KSAT.KSAT(N, M, 3, seed)
best, acc_rates = solve(ksat,mcmc_steps, anneal_steps, beta0, beta1, seed, logspace, early_stopping)

plot_acc_rates(acc_rates)