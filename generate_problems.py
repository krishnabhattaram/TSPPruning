from common import *
build_generated_problems_directory()

NUM_PROBLEMS = 10
N = 10 # number of vertices
MAX_COORDINATE = 100.0 # All coordinates selected uniformly from [0, MAX_COORDINATE)
SEED = 0
DECIMAL_PRECISION = 2

import tsplib95
import random
import os
import tqdm
random.seed(SEED)

clear_directories([GENERATED_PROBLEMS_PATH])

def random_coord():
	return round(random.random() * MAX_COORDINATE, DECIMAL_PRECISION)

for i in tqdm.trange(NUM_PROBLEMS):
	name = f'random{i + 1:06}_{N}'
	problem = tsplib95.models.StandardProblem(
		name=name,
		type='TSP',
		dimension=N,
		edge_weight_type='EUC_2D',
		display_data_type='COORD_DISPLAY',
		node_coords={
			v: (random_coord(), random_coord())
			for v in range(1, N + 1)
		}
	)
	# tsplib95's parsing is broken so we have to remove the EOF
	# or else when we load the problem again it might error
	unterminated_problem = problem.__str__()[:-3]
	with open(os.path.join(GENERATED_PROBLEMS_PATH, name + '.tsp'), 'w') as f:
		f.write(unterminated_problem)

print(f'Generated {NUM_PROBLEMS} problems')
