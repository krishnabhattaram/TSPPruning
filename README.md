# Setup
Python 3.8.4-5 had documentation [released in July 2020](https://www.python.org/doc/versions/) so we used Python 3.8.

First setup:
```
cd optlearn
python3.8 -m venv optlearn_env
source optlearn_env/bin/activate
pip3 install -r requirements.txt
```

Subsequent setups:
```
cd optlearn
source optlearn_env/bin/activate
```

# Feature Extraction Demo
1. Download a problem instance (file with extension `.tsp.gz`) from [TSPLIB95's symmetric TSP list](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/).
2. Extract the `.tsp` file and place it in `optlearn/tsplib-data/problems/`.
3. Run the extraction demo:
```
python3.8 extraction_demo.py
```
