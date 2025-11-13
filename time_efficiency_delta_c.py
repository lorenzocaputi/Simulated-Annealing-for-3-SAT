import numpy as np
import time

from KSAT import KSAT

# evaluate efficiency of code
probl = KSAT(40, 50, 30, seed=7)
n = 10000

scores1 = np.zeros(n)

start1 = time.time()
for i in range(n):
    move = probl.propose_move()
    delta_c_naive = probl.naive_delta_cost(move)
    scores1[i] = delta_c_naive
end1 = time.time()

scores2 = np.zeros(n)

start2 = time.time()
for i in range(n):
    move = probl.propose_move()
    delta_c = probl.compute_delta_cost(move)
    scores2[i] = delta_c

end2 = time.time()

print(f"time naive: {end1 - start1}")
print(f"time efficient: {end2 - start2}")
res = scores1!=scores2
print(res.sum())

# so the efficient implementation is about 18x faster
