import os

DATA_DIR = os.path.dirname(__file__) + '/tsplib-data'
PROBLEMS_DIR = os.path.join(DATA_DIR, 'problems')
FEATURES_DIR = os.path.join(DATA_DIR, 'npy')
# See the functions dict (line 478) in ./optlearn/optlearn/feature/features.py
# For any feature computation function named compute_fX_edges, you can add fX here
DESIRED_EDGE_FEATURES = ['fa', 'fb', 'fc', 'fd', 'fe', 'ff']
DRAW = False # Display edges with weights and features in build_features

# 1. Builds features directories
from optlearn.experiments.build_data import build_features
build_features(FEATURES_DIR, PROBLEMS_DIR, DESIRED_EDGE_FEATURES)

from optlearn.data.data_utils import dataLoader
# FULL_FEATURE_NAMES = [f'compute_{name}_edges' for name in DESIRED_EDGE_FEATURES]
loader = dataLoader([]) # how can we input the data_pairs if we don't have the data yet?

from networkx import draw
from optlearn.graph_utils import get_edges
from optlearn.io_utils import optObject
# Note: optlearn.plotting.plot_graph can only show one feature per plot
# from optlearn.plotting import plot_graph
for problem_file_name in os.listdir(PROBLEMS_DIR):
	# 2. Prints features
	print(f'Features for {problem_file_name}:')
	print(DESIRED_EDGE_FEATURES)
	feature_file_name = problem_file_name.replace('.tsp', '.npy')
	features_data = loader.load_features([
		os.path.join(FEATURES_DIR, feature, feature_file_name)
		for feature in DESIRED_EDGE_FEATURES])
	print(features_data)
	# 3. Plots each feature as a separate graph
	problem_file_path = os.path.join(PROBLEMS_DIR, problem_file_name)
	# graph = tsplib95.load(problem_file_path).get_graph()
	# Returns graph with N(N - 1) edges (all directed edges besides loops)
	graph = optObject().read_problem_from_file(problem_file_path).get_graph()
	edges = get_edges(graph)
	print(edges)
	for edge_idx, (u, v) in enumerate(edges):
		for feature_idx, feature in enumerate(DESIRED_EDGE_FEATURES):
			graph[u][v][feature] = features_data[edge_idx][feature_idx]
	draw(graph, withlabels=True)
