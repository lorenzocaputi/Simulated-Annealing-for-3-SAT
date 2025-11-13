import numpy as np
from copy import deepcopy

# BRIEF SUMMARY OF VARIABLES
# N: number of variables in the problem
# M: number of clauses
# K: number of constraints in each clause
# S: signs expected in each position
# index: variable that shows up in each position
# clauses: for every variable, indeices of clauses in which it shows up 

class KSAT:
    def __init__(self, N, M, K, seed = None):
        if not (isinstance(K, int) and K >= 2):
            raise Exception("k must be an int greater or equal than 2")
        self.K = K
        self.M = M
        self.N = N

        ## Optionally set up the random number generator state
        if seed is not None:
            np.random.seed(seed)
    
        # s is the sign matrix
        s = np.random.choice([-1,1], size=(M,K))
        
        # index is the matrix reporting the index of the K variables of the m-th clause 
        index = np.zeros((M,K), dtype = int)        
        for m in range(M):
            index[m] = np.random.choice(N, size=(K), replace=False)
            
        # Dictionary for keeping track of literals in clauses
        clauses = []   
        for n in range(N):
            clauses.append([i for i, row in enumerate(index) if n in row])
        
        self.s, self.index, self.clauses = s, index, clauses        
        
        ## Initialize the configuration
        x = np.ones(N, dtype=int)
        self.x = x
        self.init_config()

    ## Initialize (or reset) the current configuration
    def init_config(self):
        N = self.N 
        self.x[:] = np.random.choice([-1,1], size=(N))
        
        
    ## Definition of the cost function
    # Here you need to complete the function computing the cost using eq.(4) of pdf file
    def cost(self):
        s, x, index = self.s, self.x, self.index

        # vectorized form 2 (the fastest):
        # 1. for every clause m, do x[index[m]] to get the choices matched
        # 2. look at choice * s[m] and check that there is at least one 1
        # 3. for instance with "1 in " or max == 1 or .sum > -K
        
        choices = x[index]
        res = np.max(choices * s, axis=1)
        not_sat = (res==-1)
        c = not_sat.sum()  
        
        return c 

    def cost_np_prod(self):
        # vectorized form 1 (with np.prod):
        s, x, index = self.s, self.x, self.index
        choices = x[index]
        m = (1 - s * choices)/2
        mp = np.prod(m, 1)
        res = np.sum(mp)  

        return res  
    
    def cost_for_loop(self):
        M, K, s, x, index = self.M, self.K, self.s, self.x, self.index
        # for loop implementation (very slow):
        c = 0
        for m in range(M):
            sat = 1
            for k in range(K):
                var = index[m,k]
                sat *= (1 - s[m,k]*x[var])/2
            c += sat
        
        return c
                
      
    ## Propose a valid random move. 
    def propose_move(self):
        N = self.N
        move = np.random.choice(N)
        return move
    
    ## Modify the current configuration, accepting the proposed move
    def accept_move(self, move):
        self.x[move] *= -1
        
    def naive_delta_cost(self, move):
        old_c = self.cost()
        new_probl = self.copy()
        new_probl.accept_move(move)
        new_c = new_probl.cost()
        
        return new_c - old_c
        

    ## Compute the extra cost of the move (new-old, negative means convenient)
    # Here you need complete the compute_delta_cost function as explained in the pdf file
    def compute_delta_cost(self, move):
        M, K, s, x, index, clauses = self.M, self.K, self.s, self.x, self.index, self.clauses
        
        # find all clauses in which var is involved
        
        mask = clauses[move]
        s_masked, index_masked = s[mask], index[mask]
        
        # compute the cost from these clauses
        choices = x[index_masked]
        res = np.max(choices * s_masked, axis=1)
        not_sat = (res==-1)
        c_old = not_sat.sum()
        
        # change the var
        x[move] *= -1
        
        # recompute the score of these clauses
        choices = x[index_masked]
        res = np.max(choices * s_masked, axis=1)
        not_sat = (res==-1)
        c_new = not_sat.sum()
        
        x[move] *= -1
        
        # return the difference
        return c_new - c_old
    

    ## Make an entirely independent duplicate of the current object.
    def copy(self):
        return deepcopy(self)
    
    ## The display function should not be implemented
    def display(self):
        pass

    

