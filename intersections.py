import pandas as pd 
from KSAT_functions import find_intersection

"""
Use this file to compute the intersections between the solving probability curves 
and the P = 0.5 line to find the algorithmic threshold.
This simple method applies linear interpolation to find an estimate for the algorithmic
threshold.
"""


# load the csv file with the results
data = pd.read_csv("data.csv", index_col=None, sep=";")

# very quick data cleaning to remove unwanted columns
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
data = data[(data["mcmc"] == 1000) & (data["anneal"] == 100)]
data.sort_values(by=["N", "M"], ascending=True, inplace=True)

# extract the values of the solving probabilities from the csv file
P200 = (1.0, 1.0, 0.77, 0.47, 0.13, 0.0, 0.0)
M200 = (650, 700, 750, 800, 850, 900, 950)
P300 = data[data["N"]==300]["P"]
M300 = data[data["N"]==300]["M"]
P400 = data[data["N"]==400]["P"]
M400 = data[data["N"]==400]["M"]
P500 = data[data["N"]==500]["P"]
M500 = data[data["N"]==500]["M"]
P600 = data[data["N"]==600]["P"]
M600 = data[data["N"]==600]["M"]

# compute the intersections with linear interpolation
intersections_200 = find_intersection(M200, P200)
intersections_300 = find_intersection(M300, P300)
intersections_400 = find_intersection(M400, P400)
intersections_500 = find_intersection(M500, P500)
intersections_600 = find_intersection(M600, P600)

# Print the results
print("Intersection points:")
print("N=200:", intersections_200)
print("N=300:", intersections_300)
print("N=400:", intersections_400)
print("N=500:", intersections_500)
print("N=600:", intersections_600)
