import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Get current workding directory
cwd = os.getcwd()

# Get relative path of src directory
src_path = cwd.split('/scripts')[0]

# Add relative path to system path
sys.path.insert(0, src_path)

# Import package modules
try:
    import utils.functions as fn
    from models.event import Event
except:
    print("Failed to import module packages. Check whether relative path to /src is correct:")
    print(src_path)


# =============================
# Load and plot example event
# =============================

# Path to local data directory /lcd
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')

print(lcd_path)

