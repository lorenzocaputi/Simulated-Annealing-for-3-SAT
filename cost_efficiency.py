import numpy as np
import time

from KSAT import KSAT

# evaluate efficiency of code
probl = KSAT(40, 50, 30)
n = 10000

cost1 = np.zeros(n)

start1 = time.time()
for i in range(n):
    c1 = probl.cost()
    move = probl.propose_move()
    probl.accept_move(move)
    cost1[i] = c1
end1 = time.time()

cost2 = np.zeros(n)

start2 = time.time()
for i in range(n):
    c2 = probl.cost_np_prod()
    move = probl.propose_move()
    probl.accept_move(move)
    cost2[i] = c2

end2 = time.time()

print(f"time 1: {end1 - start1}")
print(f"time 2: {end2 - start2}")
res = cost1!=cost2
print(res.sum())


# so the first implementation is around 20% faster
