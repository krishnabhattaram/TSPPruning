# Setup
## Installation
Run the following commands:
```
python3.10 -m venv venv_tsp
source venv_tsp/bin/activate
pip3 install .
pip install --no-deps tsplib95==0.7.1
```

## Setup after Installation
Reactivate the virtual environment:
```
source venv_tsp/bin/activate
```

## Notes
We upgraded to Python 3.10 (End of support October 2026) and upgraded most of the pip packages to their most recent versions so we can develop with the newest features.

Create a virtual environment and install all pip requirements in a virtual environment. If you're not on bash/zsh, replace the 2nd command with [the activation command for your platform/shell](https://docs.python.org/3.10/library/venv.html).

tsplib95's last release was in 2020, so it relies on a very old networkx version that doesn't have all the visualization features we use. We need to install it separately so it doesn't conflict with our networkx. It may display an error but should still work.

# Workflow
## Archiving Data
You can archive the training data in `/data` with a command like this:
```
tar -zcvf training.tar.gz training/
```

## Note: These are outdated

## Steps
1. Generate a large number of random problems using `generate_problems.py`.
2. Build the features and labels using [build_features_and_labels.ipynb](build_features_and_labels.ipynb).
3. Train a neural network (currently a LogReg model) using [optlearn_model_training.py](optlearn_model_training.py).

## Notes for iPython Notebook Steps
If you modify any external Python modules (ex. in the optlearn library), to load the changes, you'll need to restart the kernel before the next run.

All code blocks are dependencies of future blocks unless otherwise noted.

# Data
## TSPLIB95 File Standard
See the [standard](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) to understand the file formats.

## Special TSP instances
We've included some handpicked special problem instances as specific examples in `tsplib-data/problems-special/`:

| Problem name | Vertices | Directed? | Description |
|---|---|---|---|
|small4_undirected|4|No|A small undirected metric graph whose edge weights are all distinct integers|
|small4_directed|4|Yes|small4_undirected but with each undirected edge split into 2 same-weight directed edges|
|ulysses16|16|No|The symmetric TSP instance from TSPLIB95 with smallest n that also had an optimal tour available on the website|
|small_tsp_instance|4|Yes|A small example graph we made with distinct integer weights (note: not metric since it breaks the triangle inequality)|

# Features
These tables organize the list of all features implemented by optlearn, which is in the end of [features.py](optlearn/feature/features.py).

## Edge
These are the features that our workflow currently supports. They are implemented by optlearn as the function `compute_<Short Name>_edges` (ex. `f1` is implemented by `compute_f1_edges`.)
<table>
    <thead>
        <tr>
            <th>Short Name</th>
            <th>Papers</th>
            <th>Description</th>
			<th>Restrictions</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>f1</td><td></td><td></td><td></td></tr>
		<tr><td>f2</td><td></td><td></td><td></td></tr>
		<tr><td>f3</td><td></td><td></td><td></td></tr>
		<tr><td>f4</td><td></td><td></td><td></td></tr>
		<tr><td>f5</td><td></td><td></td><td></td></tr>
		<tr><td>f6</td><td></td><td></td><td></td></tr>
		<tr>
            <td>f7</td>
			<td>Wang and Remmel 2018</td>
			<td>Fast estimated quadrilateral frequencies for each edge</td>
			<td></td>
        </tr>
		<tr><td>f8</td><td></td><td></td><td></td></tr>
		<tr>
			<td>f9</td>
			<td>Fitzpatrick 3.2 (MODIFIED FROM THE ORIGINAL PAPER - SEE fg_edges)</td>
			<td>Indicator features 1 or 0 from MWST</td>
			<td></td>
		</tr>
		<tr><td>f10</td><td></td><td></td><td></td></tr>
		<tr><td>f11</td><td></td><td></td><td></td></tr>
		<tr><td>f12</td><td></td><td></td><td></td></tr>
		<tr><td>f13</td><td></td><td></td><td></td></tr>
		<tr>
            <td>fa</td>
			<td rowspan=6>Fitzpatrick 3.3 eqns (7)-(12), originally from Sun</td>
			<td>The comparison of the current edge weight to the global graph.</td>
			<td rowspan=6>None</td>
        </tr>
		<tr>
			<td>fb</td>
			<td>The comparison of the current edge weight to its max left neighbor.</td>
		</tr>
		</tr>
		<tr>
			<td>fc</td>
			<td>The comparison of the current edge weight to its max right neightbor.</td>
		</tr>
		</tr>
		<tr>
			<td>fd</td>
			<td>Comparison of the edge weight to the overall graph (divide by global max).</td>
		</tr>
		<tr>
			<td>fe</td>
			<td>Compare the edge weight to its minimum left neighbor</td>
		</tr>
		<tr>
			<td>ff</td>
			<td>Compare the edge weight to its minimum right neighbor</td>
		</tr>
		<tr>
			<td>fg</td>
			<td>Fitzpatrick 3.2</td>
			<td>Continuous features corresponding to 0 or the MST iteration at which this edge was removed</td>
			<td>Undirected graphs only</td>
		</tr>
		<tr>
			<td>fh</td>
			<td></td>
			<td></td>
			<td></td>
		</tr>
		<tr>
			<td>fi</td>
			<td rowspan=2>Fitzpatrick 3.1</td>
			<td>r^ - Standardization of the reduced costs vector rk, calculated through subtour elimination constraints</td>
			<td rowspan=2>None</td>
		</tr>
		<tr>
			<td>fj</td>
			<td>r~ - Mean of all normalized reduced costs from k perturbed copies of the original LP relaxation after removing subtours</td>
		</tr>
		<tr><td>fk</td><td></td><td></td><td></td></tr>
		<tr><td>fp</td><td></td><td></td><td></td></tr>
		<tr><td>fm</td><td></td><td></td><td></td></tr>
    </tbody>
</table>

## Vertex
These are currently **not** supported by our workflow. They are implemented by optlearn as the function `compute_<Short Name>_vertices` (ex. `f1` is implemented by `compute_f1_vertices`.)
<table>
    <thead>
        <tr>
            <th>Short Name</th>
            <th>Papers</th>
            <th>Description</th>
			<th>Restrictions</th>
        </tr>
    </thead>
    <tbody>
		<tr><td>f1</td><td></td><td></td><td></td></tr>
		<tr><td>f2</td><td></td><td></td><td></td></tr>
		<tr><td>f3</td><td></td><td></td><td></td></tr>
		<tr><td>f4</td><td></td><td></td><td></td></tr>
    </tbody>
</table>
