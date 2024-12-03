# Setup
We upgraded to Python 3.10 (End of support October 2026) and upgraded most of the pip packages to their most recent versions so we can develop with the newest features.

**All commands must be run in the `optlearn` directory so modules can find the venv.**

**If using VS Code, either open the workspace to `optlearn` to automatically set the interpreter path, or manually set the interpreter path to `./optlearn/optlearn_env/bin/python`.**

## First time using TSPPruning after download
Enter the top `optlearn` directory if you're not already in it:
```
cd optlearn
```

Install all pip requirements:
```
python3.10 -m venv optlearn_env
source optlearn_env/bin/activate
pip install -r requirements.txt
```

tsplib95's last release was in 2020, so it relies on a very old networkx version that doesn't have all the visualization features we use. Install it separately so it doesn't conflict with our networkx:
```
pip install --no-deps tsplib95==0.7.1
```
It may display an error but should still work.

## Second time and afterwards
If using VS Code, just select the venv. From the CLI, enter the first optlearn package and source the activate script:
```
source optlearn_env/bin/activate
```

# Data
## TSPLIB95 File Standard
See the [standard](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) to understand the file formats.

## Special TSP instances
We've included some handpicked special problem instances as specific examples in `optlearn/tsplib-data/problems-special/`:

| Problem name | Vertices | Directed? | Description |
|---|---|---|---|
|small4_undirected|4|No|A small undirected metric graph whose edge weights are all distinct integers|
|small4_directed|4|Yes|small4_undirected but with each undirected edge split into 2 same-weight directed edges|
|ulysses16|16|No|The symmetric TSP instance from TSPLIB95 with smallest n that also had an optimal tour available on the website|
|small_tsp_instance|4|Yes|A small example graph we made with distinct integer weights (note: not metric since it breaks the triangle inequality)|

# Features
The list of all implemented features is in the end of [features.py](/optlearn/optlearn/feature/features.py).

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Papers</th>
            <th>Description</th>
			<th>Restrctions</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>f1_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f2_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f3_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f4_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f5_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f6_edges</td><td></td><td></td><td></td></tr>
		<tr>
            <td>f7_edges</td>
			<td>Wang and Remmel 2018</td>
			<td>Fast estimated quadrilateral frequencies for each edge</td>
        </tr>
		<tr><td>f8_edges</td><td></td><td></td></tr>
		<tr>
			<td>f9_edges</td>
			<td>Fitzpatrick 3.2 (MODIFIED FROM THE ORIGINAL PAPER - SEE fg_edges)</td>
			<td>Indicator features 1 or 0 from MWST</td>
		</tr>
		<tr><td>f10_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f11_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f12_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f13_edges</td><td></td><td></td><td></td></tr>
		<tr><td>f1_vertices</td><td></td><td></td><td></td></tr>
		<tr><td>f2_vertices</td><td></td><td></td><td></td></tr>
		<tr><td>f3_vertices</td><td></td><td></td><td></td></tr>
		<tr><td>f4_vertices</td><td></td><td></td><td></td></tr>
		<tr>
            <td>fa_edges</td>
			<td rowspan=6>Fitzpatrick 3.3 eqns (7)-(12), originally from Sun</td>
			<td>The comparison of the current edge weight to the global graph.</td>
        </tr>
		<tr>
			<td>fb_edges</td>
			<td>The comparison of the current edge weight to its max left neighbor.</td>
		</tr>
		</tr>
		<tr>
			<td>fc_edges</td>
			<td>The comparison of the current edge weight to its max right neightbor.</td>
		</tr>
		</tr>
		<tr>
			<td>fd_edges</td>
			<td>Comparison of the edge weight to the overall graph (divide by global max).</td>
		</tr>
		<tr>
			<td>fe_edges</td>
			<td>Compare the edge weight to its minimum left neighbor</td>
		</tr>
		<tr>
			<td>ff_edges</td>
			<td>Compare the edge weight to its minimum right neighbor</td>
		</tr>
		<tr>
			<td>fg_edges</td>
			<td>Fitzpatrick 3.2</td>
			<td>Continuous features corresponding to 0 or the MST iteration at which this edge was removed</td>
		</tr>
		<tr>
			<td>fh_edges</td>
			<td></td>
			<td></td>
			<td rowspan=6>None</td>
		</tr>
		<tr>
			<td>fi_edges</td>
			<td rowspan=2>Fitzpatrick 3.1</td>
			<td>r^ - Standardization of the reduced costs vector rk, calculated through subtour elimination constraints</td>
		</tr>
		<tr>
			<td>fj_edges</td>
			<td>r~ - Mean of all normalized reduced costs from k perturbed copies of the original LP relaxation after removing subtours</td>
		</tr>
		<tr><td>fk_edges</td><td></td><td></td></tr>
		<tr><td>fp_edges</td><td></td><td></td></tr>
		<tr><td>fm_edges</td><td></td><td></td></tr>
    </tbody>
</table>

# Scripts
## Feature Extraction Demo
1. Add problem instances (files with extension `.tsp`) into `optlearn/tsplib-data/problems/` from one of these sources:
	1. To get it from TSPLIB, download a problem instance (file with extension `.tsp.gz`) from [TSPLIB95's symmetric TSP list](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/). Then extract the `.tsp` file.
	2. Copy one from `optlearn/tsplib-data/problems-special/`.
2. If you want to build labels as well, and you want to use precomputed solutions to skip solving time, add solutions (files with extension `.opt.tour`) into `optlearn/tsplib-data/solutions` from one of these sources:
	1. Similarly, you can download one from the same source as above. WARNING: Some of the tour files have all the indices in the `TOUR_SECTION` on the same line, which may cause an error. To fix this, place each index on a new line.
	2. Copy one from `optlearn/tsplib-data/solutions-special/`.
3. Choose desired features from the [features list](#Features).
4. Run the extraction demo in `extraction_demo.ipynb`.
5. You'll get visualizations of the weights and features. Also, the features and solutions should appear in `optlearn/tsplib-data/npy` in numpy format.

## Execution Flow
(To help devs debug)
1. `experiments.build_data.build_features()`
	1. `self.data_create()` (At this point, `self = data.data_utils.createTrainingFeatures`)
		1. For each problem `name`:
			1. `self.data_steps(name)` 
				1. For each feature name `function_name`:
					1. `self.feature_step()`
						1. `self.load_object()` (sets `self._graph` to the Graph object for this problem)
						2. `features.functions[function_name]()` (compute the feature function)
						3. `self.write_to_npy()`
