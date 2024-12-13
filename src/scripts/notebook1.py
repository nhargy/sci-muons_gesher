import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy

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
except Exception as e:
    print("Failed to import module packages. Check whether relative path to /src is correct:")
    print(src_path)
    print(e)

# Define important paths
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')
out_path  = os.path.join(repo_path, 'out')
plt_path  = os.path.join(repo_path, 'plt')


# ================
# Event analysis
# ================
"""
In the following example we will load an event just as in example1,
then do some analysis on it.
"""

# Define path to pdf
pdf_path      = os.path.join(out_path, 'notebook1.pdf')

# Initialise pdf
pdf           = PdfPages(pdf_path)

# Define path to specific run
dir_path      = 'VS1/Run3'
run_path = os.path.join(lcd_path, dir_path)

# Define scope_config
scope_config  = [('scope-1-run3', 4) ,('scope-2-run3', 4)]
"""
scope_config: each tuple specifies the scope name as given in the saved csv files
              and the corresponding number of active channels. 
"""

# Choose segment, or define it as system input
#segment       = 100
segment       = sys.argv[1]

# Define event object
myevent       = Event(run_path, segment, scope_config)

# Process event data and store in variable
myevent.get_data()
mydata = myevent.data     # waveform matrix of all channels
times  = myevent.times    # the x-axis time values, one array for each scope


# ==========
# Analysis
# ==========

# Correct baseline
for num, row in enumerate(mydata):
    bl = fn.find_baseline(row)[0]
    wf = row - bl
    mydata[num] = wf

t   = times[0]
wf1 = mydata[0]
wf2 = mydata[1]

a   = np.argmin(np.abs(t - -50))
b   = np.argmin(np.abs(t - 75))

p1_idx,p1_val = fn.get_first_peak(wf1, threshold = 140, ROI=(a,b))
p2_idx,p2_val = fn.get_first_peak(wf2, threshold = 140, ROI=(a,b))
risetime1     = fn.get_risetime(t, wf1, p1_idx)
risetime2     = fn.get_risetime(t, wf2, p2_idx)

dt = np.round(risetime1 - risetime2, 2)

fig, ax = plt.subplots()

ax.plot(t, wf1)
ax.plot(t, wf2)
ax.axvline(risetime1, color = 'blue', linewidth = 0.8)
ax.axvline(risetime2, color = 'orange', linewidth = 0.8)

ax.set_xlim(-50,50)

ax.set_title(rf'$\Delta t = ${dt}ns', fontsize=20)

# Format for pdf view
fig.tight_layout()

# Save to pdf object
pdf.savefig()
plt.close()

# End entire script in closing pdf object so it can refresh
pdf.close()
