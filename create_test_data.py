import pickle
import os
import LG_1d as lg
import numpy as np
from tqdm import tqdm


"""
METRICS

N = 63, 1000 solutions with random forcing: 200.3 seconds
"""

def save_obj(obj, name):
	cwd = os.getcwd()
	path = os.path.join(cwd,'data')
	if os.path.isdir(path) == False:
		os.makedirs('data')
	with open('data/'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

SIZE = 10000
N = 63
epsilon = np.linspace(1E0, 1E-6, 100000)

data = np.zeros((SIZE, N+1))
for i in tqdm(range(100)):
	x, u = lg.lg_1d_enriched(N, np.random.choice(epsilon))
	u = u.reshape(1,u.shape[0])
	data[i,:] = u


save_obj(data, f'{SIZE}')