import os
import sys
import numpy as np

# Get current working directory
cwd        = os.getcwd()

# Get relative path sci-muon_gesher/src
src_path  = cwd.split('/models')[0]

# Add src path to system path
sys.path.insert(0, src_path)

# Import package modules
try:
    import utils.functions as fn
except:
    print('Failure to import package modules. Check whether system path is correct:')
    print(src_path)


class Run:

    def __init__(self):

        pass
