import pandas as pd 
from KSAT_functions import limiting_threshold_plot, find_intersection

"""
Use this file to plot the results from an experiment, which fixed N=200, M=200
and analyzed the impact of the choice of the optimization parameters on the 
resulting estimate of the algorithmic threshold.
It is also possible to apply a rescaling of M to M/N, to see the curves 
collapsing on the same plot.
"""

# load the csv file with the results
data = pd.read_csv("psat.csv", index_col=None, sep=";")

# very quick data cleaning to remove unwanted columns, and sorting for plotting purposes
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
data.sort_values(by=["N", "M"], ascending=True, inplace=True)

# extract all the results from the csv file
mcmc_list = (1000, 2000, 3000, 4000, 5000)
colors = ("dodgerblue", "gold", "green", "orange", "purple")

def extract_data(data):
    d = dict()
    for i, mcmc in enumerate(mcmc_list):
        d[mcmc] = (data[data["mcmc"]==mcmc]["M"], data[data["mcmc"]==mcmc]["P"], colors[i])
    return d

## Create a dictionary to store the data in a cleaner format and put it all in one plot
# to apply the rescaling and collapse the curves, set rescaling to True


d = extract_data(data)

for key in d:
    intersection = find_intersection(d[key][0], d[key][1])
    print(f"Algorithmic threshold for mcmc={key}: {intersection/200}")

limiting_threshold_plot(d, rescaling=False)





