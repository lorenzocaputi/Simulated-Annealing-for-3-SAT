import KSAT
from KSAT_functions import solve, multi_plot

"""
Use this file to solve multiple instances of the K-SAT problem 
for a single fixed N and a single fixed M, but testing different 
values of mcmc_steps and anneal_steps.
Also plots the evolution of the acceptance rates for each instance
and combines them into a single multi-plot figure
"""

seed = 42

# problem variables
N = 200
M = 200
K = 3

# optimization parameters (set low for demonstration since it runs for quite a long time)
mcmc_steps_list = (10, 50, 100)
anneal_steps_list = (10, 20, 50)
beta0 = 0.1
beta1 = 10
logspace = False        # if set to True, the betas in the annealing schedule are logarithmically spaced (log10)
early_stopping = False  # this stops the optimization as soon as a solution is found

acc_rates_matrix = [[None, None, None], 
                    [None, None, None], 
                    [None, None, None]]


# plot a multi-figure plot 

ksat = KSAT.KSAT(N, M, K, seed)

for i, mcmc_steps in enumerate(mcmc_steps_list):
    for j, anneal_steps in enumerate(anneal_steps_list):
        _, acc_rates = solve(ksat, mcmc_steps, anneal_steps, beta0, beta1, seed, logspace, early_stopping)
        acc_rates_matrix[i][j] = acc_rates


multi_plot(acc_rates_matrix, len(mcmc_steps_list), len(anneal_steps_list))
