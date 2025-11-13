from KSAT_functions import solve_multiple_M, plot_multiple_acc_rates

"""
Use this file to solve multiple instances of the K-SAT problem 
for a fixed N and arbitrary list of M_s and plot the evolution of 
the acceptance rates for each instance
"""

seed = 42

# problem variables
N = 200
M = (200, 400, 600, 800, 1000)
K = 3

# optimization parameters (can set lower for demonstration purposes)
mcmc_steps = 1000
anneal_steps = 100
beta0 = 0.1
beta1 = 10
logspace = False        # if set to True, the betas in the annealing schedule are logarithmically spaced (log10)
early_stopping = False  # this stops the optimization as soon as a solution is found


solutions, acc_rates_dict = solve_multiple_M(N, M, K, mcmc_steps, anneal_steps, beta0, beta1, seed, logspace, early_stopping)

plot_multiple_acc_rates(acc_rates_dict)