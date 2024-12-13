# =============
# delta_t_2.py
# =============
#
# Visualises the delta-t on a scintillator plate from signal.


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy
from scipy import interpolate

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
    print("From system error ==> ", e)


# Define important paths
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')
out_path  = os.path.join(repo_path, 'out')
plt_path  = os.path.join(repo_path, 'plt')

# Define path to live pdf
pdf_path = os.path.join(out_path, 'delta_t_2.pdf')

# Initialise pdf
pdf      = PdfPages(pdf_path)

# Define path to specific run
dir_path = 'VS1/Run5'
run_path = os.path.join(lcd_path, dir_path)

scope_config = [('scope-1-run5', 4),('scope-2-run5', 4)]

seg = sys.argv[1]

def delta_t(times, wf1, wf2, ROI, thresh=120):

    # Find first relevant peak
    peak1_idx, egress1_idx = fn.find_peak(wf1, thresh, ROI)
    peak2_idx, egress2_idx = fn.find_peak(wf2, thresh, ROI)

    peak1_val = wf1[peak1_idx]
    f1        = interpolate.interp1d(wf1[:peak1_idx-5], t[:peak1_idx-5])
    t1        = f1(peak1_val/10)

    peak2_val = wf2[peak2_idx]
    f2        = interpolate.interp1d(wf2[:peak2_idx-5], t[:peak2_idx-5])
    t2        = f2(peak2_val/10)


    if peak1_idx and peak2_idx != None:
        dt = times[egress1_idx] - times[egress2_idx]
        print(np.round(t1-t2,2))
    else:
        dt = None

    return egress1_idx, egress2_idx, dt


myevent = Event(run_path, seg, scope_config)
myevent.get_data()
mydata = myevent.data
times  = myevent.times

# Zero baselines:
for num, row in enumerate(mydata):
    bl = fn.find_baseline(row)[0]
    wf = row - bl
    mydata[num] = wf

# find_peak kwargs
thresh=120
ROI=(140,280)

wf1 = mydata[0]
wf2 = mydata[1]
t   = times[0]

fig, ax = plt.subplots(figsize=(6, 3.5))

ax.plot(t, wf1)
ax.plot(t, wf2)
ax.axvspan(t[ROI[0]], t[ROI[1]], color = 'lawngreen', alpha = 0.25)
ax.axvline(0, linestyle='--', color='grey', alpha=0.5)

eg1, eg2, mydt = delta_t(t, wf1, wf2, ROI=ROI)

if eg1 and eg2 != None:
    ax.scatter(t[eg1], wf1[eg1], color='blue')
    ax.scatter(t[eg2], wf2[eg2], color='orange')

    ax.set_title(rf'$\Delta t$ = {np.round(mydt,2)} ns')

#ax.set_xlim(t[ROI[0]]-10,t[ROI[1]]+10)

pdf.savefig()
plt.close()

# ====
pdf.close()
