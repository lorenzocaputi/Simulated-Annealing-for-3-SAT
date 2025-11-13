import pandas as pd 
from KSAT_functions import plot_multiple_probabilities

"""
Use this file to plot the solving probabilities for increasing values of M,
and for different values of N, all in the same plot.
It is also possible to apply a rescaling of M to M/N, to see the curves 
collapsing on the same plot.

"""

# load the csv file with the results
data = pd.read_csv("data.csv", index_col=None, sep=";")

# very quick data cleaning to remove unwanted columns, and sorting for plotting purposes
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
data = data[(data["mcmc"] == 1000) & (data["anneal"] == 100)]
data.sort_values(by=["N", "M"], ascending=True, inplace=True)


# I run numerous tests at N = 200, so I hand picked the same number of runs as for the other values of N,
# to have a cleaner plot (very similar results can be obtained with all the data for N=200, 
# provided mcmc_steps and annealing_steps are kept the same) 
P200 = (1.0, 1.0, 0.77, 0.47, 0.13, 0.0, 0.0) 
M200 = (650, 700, 750, 800, 850, 900, 950)


# extract all the results from the csv file
P300 = data[data["N"]==300]["P"]
M300 = data[data["N"]==300]["M"]
P400 = data[data["N"]==400]["P"]
M400 = data[data["N"]==400]["M"]
P500 = data[data["N"]==500]["P"]
M500 = data[data["N"]==500]["M"]
P600 = data[data["N"]==600]["P"]
M600 = data[data["N"]==600]["M"]


## Create a dictionary to store the data in a cleaner format and put it all in one plot
# to apply the rescaling and collapse the curves, set rescaling to True

dict = {200: (M200, P200, 'dodgerblue'), 300: (M300, P300, 'gold'), 
        400: (M400, P400, "green"), 500: (M500, P500, "orange"), 
        600: (M600, P600, "purple")}

plot_multiple_probabilities(dict, rescaling=True)
