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

# Scripts

## Feature Extraction Demo
1. Add a problem instance (file with extension `.tsp`) into `optlearn/tsplib-data/problems/` from one of these sources:
	1. To get it from TSPLIB, download a problem instance (file with extension `.tsp.gz`) from [TSPLIB95's symmetric TSP list](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/). Then extract the `.tsp` file.
	2. To use one of our special problem instances, copy it from `optlearn/tsplib-data/problems-special/`.
3. Choose desired features from the end of [features.py](/optlearn/optlearn/feature/features.py).
4. Run the extraction demo:
```
python3.8 extraction_demo.py
```
5. After a few minutes, the features and solutions should appear in `optlearn/tsplib-data/npy` in numpy format.

## iPython Notebook
I tried running this flow in an iPython notebook (`extraction_demo.ipynb`) but ran into errors when trying to do the pip installs in the same way.

Theoretically, I can follow [this post](https://stackoverflow.com/a/64105223) to run everything using the existing optlearn_env.