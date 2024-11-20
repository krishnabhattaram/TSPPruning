# Setup
Python 3.8.4-5 had documentation [released in July 2020](https://www.python.org/doc/versions/) so we used Python 3.8.

## First time using TSPPruning after download
Install all pip requirements:
```
cd optlearn
python3.8 -m venv optlearn_env
source optlearn_env/bin/activate
pip3 install -r requirements.txt
```

## Second time and afterwards
Just enter the first optlearn package and source the activate script:
```
cd optlearn
source optlearn_env/bin/activate
```

# Features
The list of all implemented features is in the end of [features.py](/optlearn/optlearn/feature/features.py).

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Papers</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>f1_edges</td><td></td><td></td></tr>
		<tr><td>f2_edges</td><td></td><td></td></tr>
		<tr><td>f3_edges</td><td></td><td></td></tr>
		<tr><td>f4_edges</td><td></td><td></td></tr>
		<tr><td>f5_edges</td><td></td><td></td></tr>
		<tr><td>f6_edges</td><td></td><td></td></tr>
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
		<tr><td>f10_edges</td><td></td><td></td></tr>
		<tr><td>f11_edges</td><td></td><td></td></tr>
		<tr><td>f12_edges</td><td></td><td></td></tr>
		<tr><td>f13_edges</td><td></td><td></td></tr>
		<tr><td>f1_vertices</td><td></td><td></td></tr>
		<tr><td>f2_vertices</td><td></td><td></td></tr>
		<tr><td>f3_vertices</td><td></td><td></td></tr>
		<tr><td>f4_vertices</td><td></td><td></td></tr>
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
		<tr><td>fh_edges</td><td></td><td></td></tr>
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
1. Add a problem instance (file with extension `.tsp`) into `optlearn/tsplib-data/problems/` from one of these sources:
	1. To get it from TSPLIB, download a problem instance (file with extension `.tsp.gz`) from [TSPLIB95's symmetric TSP list](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/). Then extract the `.tsp` file.
	2. To use one of our special problem instances, copy it from `optlearn/tsplib-data/problems-special/`.
3. Choose desired features from the [features list](#Features).
4. Run the extraction demo:
```
python3.8 extraction_demo.py
```
5. After a few minutes, the features and solutions should appear in `optlearn/tsplib-data/npy` in numpy format.

## Execution Flow
1. `experiments.build_data.build_features()`
	1. `self.data_create()` (At this point, `self = data.data_utils.createTrainingFeatures`)
		1. For each problem `name`:
			1. `self.data_steps(name)` 
				1. For each feature name `function_name`:
					1. `self.feature_step()`
						1. `self.load_object()` (sets `self._graph` to the Graph object for this problem)
						2. `features.functions[function_name]()` (compute the feature function)
						3. `self.write_to_npy()`

## iPython Notebook
I tried running this flow in an iPython notebook (`extraction_demo.ipynb`) but ran into errors when trying to do the pip installs in the same way.

Theoretically, I can follow [this post](https://stackoverflow.com/a/64105223) to run everything using the existing optlearn_env.

## Feature Calculation
Commenting out lines `264-265` causes the optlearn workflow to calculate strictly the features overgoing needless computation to solve the TSP problem instance. 
