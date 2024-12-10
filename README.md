# sci-muons_gesher

**A Weizmann Institute of Science Project**

## Getting Started

1. Clone the repository locally
```
git clone https://github.com/nhargy/sci-muons_gesher.git
```

2. Open struct.sh inside a text editor. Scroll down to the following lines:
```
# ==========================================================
# Employing IF_bin_to_csv.py to convert binary files to csv
# ==========================================================

# Local path to Gesher_Muons data folder (modify for your local machine)
DATA_PATH=/home/hargy/Science/DataBox

# Local path to sci-mions_gesher repo (modify for your local machine)
REPO_PATH=/home/hargy/Science/Projects
```
DATA_PATH should point to where the 'Gesher_Muons' data folder is saved locally, and REPO_PATH should point to where this repo is cloned locally.

2. Setup local project structure, local data conversions and python virtual environment
```
chmod +x struct.sh
./struct.sh
```

3. Activate virtual environment
```
source venv/bin/activate
```

4. Install python dependencies from requirements.txt
```
pip3 install -r requirements.txt
```

## Files

lcd = 'local data'
plt = 'plots'
out = 'output'
src = 'source code'
venv = 'python virtual environment'
