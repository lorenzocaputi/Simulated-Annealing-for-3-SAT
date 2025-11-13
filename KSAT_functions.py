import SimAnn
import KSAT

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

seed = 42

"""
This file contains all the functions used across other files for the report, along with a brief
description of their scope.
"""


def solve(ksat, mcmc_steps, anneal_steps, beta0, beta1, seed=seed, logspace=False, early_stopping=True):

    """Solve a single instance of the K-SAT problem running SimAnn"""

    best, acc_rates = SimAnn.simann(ksat,
                          mcmc_steps = mcmc_steps, anneal_steps = anneal_steps,
                          beta0 = beta0, beta1 = beta1,
                          seed = seed,
                          debug_delta_cost = False,
                          logspace=logspace,
                          early_stopping = early_stopping)
    return best, acc_rates


def solve_multiple_M(N, M:list, K, mcmc_steps, anneal_steps, beta0, beta1, seed, logspace, early_stopping):

    """Solve multiple instances of K-SAT for a fixed value of N and a list of M_s"""

    acc_rates_dict = dict()
    solutions = []
    for m in M:
        print(f"\nsolving {K}-SAT with {N} variables and {m} clauses:\n")
        ksat = KSAT.KSAT(N, m, K, seed)
        best, acc_rates = solve(ksat, mcmc_steps, anneal_steps, beta0, beta1, seed, logspace, early_stopping)
        solutions.append(best)
        acc_rates_dict[m] = acc_rates


    return solutions, acc_rates_dict


def plot_acc_rates(acc_rates):

    """Plot the evolution of the acceptance rate during the optimization of a single instance of the K-SAT problem"""

    # Obtain only rates and steps
    rates = [rate for beta, rate in acc_rates]
    steps = list(range(len(acc_rates)))
    
    # actual plotting
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(9, 6))
    plt.plot(steps, rates, linestyle='-', color='dodgerblue', label="Acceptance Rate")
    
    # Labels and title
    plt.xlabel('Annealing Step', fontsize=14, labelpad=10)
    plt.ylabel('Acceptance Rate', fontsize=14, labelpad=10)
    plt.title('Evolution of the Acceptance Rate', fontsize=16, pad=15)
    
    # Figure features
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12, loc='best')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Display
    plt.tight_layout()
    plt.show()


def plot_multiple_acc_rates(acc_rates_dict):
    
    """Plots the evolution of the acceptance rate during the optimizations for different instances of K-SAT,
    assuming each is run with the same value for N and different values of M"""

    # Set figure
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(6*1.44, 6))
    
    # Iterate over each problem instance and plot the acc_rate curve
    for clauses, acc_rates in acc_rates_dict.items():
        rates = [rate for beta, rate in acc_rates]
        steps = list(range(len(acc_rates)))
        plt.plot(steps, rates, linestyle='-', label=f"{clauses} Clauses")
    
    # Labels and title
    plt.xlabel('Annealing Step', fontsize=14, labelpad=10)
    plt.ylabel('Acceptance Rate', fontsize=14, labelpad=10)
    plt.title('Evolution of Acceptance Rate', fontsize=16, pad=15)
    
    # Figure features
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12, title="Problem Instances")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Display
    plt.tight_layout()
    plt.show()


def multi_plot(acc_rates_matrix, rows, cols):
    """
    Plots multiple subplots with individual axis labels in a grid layout.
    Each subplot corresponds to the evolution of the acceptance rate for a given choice of the optimization parameters
    
    Parameters:
    acc_rates (list of tuples): List of tuples where each tuple contains a beta and a rate.
    rows (int): Number of rows in the grid.
    cols (int): Number of columns in the grid.
    """
    # Set Figure
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4*0.75, rows * 3*0.75))
    
    # Iterate over every subplot
    for i in range(rows):
        for j in range(cols):
            ax = axes[i, j]
            
            # Generate rates and steps for plotting
            rates = [rate for beta, rate in acc_rates_matrix[i][j]]
            steps = list(range(len(acc_rates_matrix[i][j])))
            
            # Plot on the current subplot
            ax.plot(steps, rates, linestyle='-', color='dodgerblue', label="Acceptance Rate")
            
            # Individual labels and titles
            ax.set_xlabel('Annealing Step', fontsize=10)
            ax.set_ylabel('Acceptance Rate', fontsize=10)
            
            # Figure features
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend(fontsize=8, loc='upper right')
            ax.tick_params(axis='both', which='major', labelsize=8)
    
    # Display
    plt.tight_layout()
    plt.show()


def plot_probability(M, P):

    """Plots the empirical solving probability of a K-SAT problem, computed at different values of M"""

    # Set figure
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(6*1.44, 6))

    # Actual plotting
    plt.plot(M, P, linestyle='-', color='dodgerblue', label="Solving probability")
    plt.axhline(y=0.5, color='red', linestyle='--', label="P=0.5")

    # Axis and labels
    plt.xlabel('Number of clauses', fontsize=14, labelpad=10)
    plt.ylabel('Solving probability', fontsize=14, labelpad=10)
    plt.title('Solving probability with increasing number of clauses', fontsize=16, pad=15)
    
    # Figure features
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12, loc='best')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Display
    plt.tight_layout()
    plt.show()


def plot_multiple_probabilities(dict, rescaling):

    """plot the solving probabilities for increasing values of M, and for different values of N, all in the same plot.
       It is also possible to apply a rescaling of M to M/N, to see the curves collapsing on the same plot."""

    # Set figure
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(6*1.44, 6))

    # Plot probabilities for each (n, m) combination
    for key in dict:
        M = dict[key][0]
        if rescaling:
            plt.plot([m/key for m in M], dict[key][1], linestyle='-', color=dict[key][2], label=f"N={key}")
        else:
            plt.plot(M, dict[key][1], linestyle='-', color=dict[key][2], label=f"N={key}")



    # Axis and labels
    plt.axhline(y=0.5, color='red', linestyle='--', label="P=0.5")
    plt.ylabel('Solving probability', fontsize=14, labelpad=10)
    if rescaling:
        plt.xlabel('Clauses-to-Variables ratio (M/N)', fontsize=14, labelpad=10)
        plt.title('Solving probability with increasing number of clauses (rescaled)', fontsize=16, pad=15)

    else:
        plt.xlabel('Number of Clauses', fontsize=14, labelpad=10)
        plt.title('Solving probability with increasing number of clauses', fontsize=16, pad=15)



    # Figure features
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12, loc='best')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Display
    plt.tight_layout()
    plt.show()

def limiting_threshold_plot(dict, rescaling):

    """plot the results from an experiment, which fixed N=200, M=200
    and analyzed the impact of the choice of the optimization parameters on the 
    resulting estimate of the algorithmic threshold."""

    # Set figure
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(6*1.44, 6))

    # Plot probabilities for each (n, m) combination
    for key in dict:
        M = dict[key][0]
        if rescaling:
            plt.plot([m/200 for m in M], dict[key][1], linestyle='-', color=dict[key][2], label=f"mcmc={key}")
        else:
            plt.plot(M, dict[key][1], linestyle='-', color=dict[key][2], label=f"N={key}")



    # Axis and labels
    plt.axhline(y=0.5, color='red', linestyle='--', label="P=0.5")
    plt.ylabel('Solving probability', fontsize=14, labelpad=10)
    if rescaling:
        plt.xlabel('Clauses-to-Variables ratio (M/N)', fontsize=14, labelpad=10)
        plt.title('Solving probability with increasing number of mcmc steps (rescaled)', fontsize=16, pad=15)

    else:
        plt.xlabel('Number of Clauses', fontsize=14, labelpad=10)
        plt.title('Solving probability with increasing number of mcmc steps', fontsize=16, pad=15)



    # Figure features
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12, loc='best')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Display
    plt.tight_layout()
    plt.show()

def find_intersection(M, P, target=0.5):

    """Applies linear interpolation to find an estimate of the algorithmic threshold"""

    M = M.to_numpy() if hasattr(M, "to_numpy") else M
    P = P.to_numpy() if hasattr(P, "to_numpy") else P

    for i in range(len(P) - 1):
        if (P[i] > target >= P[i + 1]):
            # Linear interpolation to find the intersection point
            slope = (P[i + 1] - P[i]) / (M[i + 1] - M[i])
            intersection = M[i] + (target - P[i]) / slope
            return intersection