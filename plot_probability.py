from KSAT_functions import plot_probability

""""
Use this file to plot the solving probability for a fixed N, and increasing values of M.
In this case, I plot the results of my runs for N = 200, and M varying from 650 to 950.
As always, for more information on the function "plot_probability", read the KSAT_functions file.
"""


P200 = (1.0, 1.0, 0.77, 0.47, 0.13, 0.0, 0.0) 
M200 = (650, 700, 750, 800, 850, 900, 950)


plot_probability(M200, P200)
