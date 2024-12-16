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
except:
    print("Failed to import module packages. Check whether relative path to /src is correct:")
    print(src_path)

# Define important paths
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')
out_path  = os.path.join(repo_path, 'out')
plt_path  = os.path.join(repo_path, 'plt')


# ==================
# Reconstruct Event
# ==================

# Define path to pdf
pdf_path      = os.path.join(out_path, 'recon.pdf')

# Initialise pdf
pdf           = PdfPages(pdf_path)

# Define path to specific run
dir_path      = 'VS1/Run5'
vs1_run4_path = os.path.join(lcd_path, dir_path)

# Define scope_config
scope_config  = [('scope-1-run5', 4) ,('scope-2-run5', 4)]

# Choose segment, or define it as system input
#segment       = 100
segment       = sys.argv[1]

# Define event object
event       = Event(vs1_run4_path, segment, scope_config)

# Process event data and store in variable
event.get_data()
event.zero_baselines()
data = event.data     # waveform matrix of all channels
times  = event.times    # the x-axis time values, one array for each scope

rtm = event.risetime_mtx
dta = event.dt_arr

ROI       = (-60,80)
threshold = 140
fraction  = 0.25

def calc_risetime_mtx(times, data, risetime_mtx, ROI=ROI, threshold=threshold, fraction=fraction): # would all be self.<property>
    """
    Calculates the risetime of each peak on each scintillator plate, if it exists.

    Args:
        
    Returns:
        None
        => Updates Event.risetime_mtx property.
    """
    wf_idx = 0
    for scope_idx, scope in enumerate(risetime_mtx):
        print("Scope Number: ", scope_idx+1)
        t = times[scope_idx]
        a = np.argmin(np.abs(t - ROI[0]))
        b = np.argmin(np.abs(t - ROI[1]))
        ROI_idx = (a,b)
        print("ROI: ", ROI_idx )
        for plate_idx, plate in enumerate(scope):
            print("Plate Number: ", plate_idx+1)
            wf1 = data[wf_idx]
            wf2 = data[wf_idx+1]

            p1, _ = fn.get_first_peak(wf1, threshold=threshold, ROI=ROI_idx)
            p2, _ = fn.get_first_peak(wf2, threshold=threshold, ROI=ROI_idx)
            print("Waveforms ", wf_idx+1, " and ", wf_idx+2)

            if p1 and p2 != None:
                print('YES')
                fraction  = fraction
                rt1 = fn.get_risetime(t, wf1, p1, fraction=fraction)
                rt2 = fn.get_risetime(t, wf2, p2, fraction=fraction)

                risetime_mtx[scope_idx][plate_idx][0] = rt1
                risetime_mtx[scope_idx][plate_idx][1] = rt2

            wf_idx += 2

    return None

# Test

calc_risetime_mtx(times, data, rtm)
print(rtm)

def calc_dt_arr():
    """
    Calculates the risetime difference dt between the two peaks on each scintillator plate,
    if both exist.

    Args:

    Returns:
        None
        => Updates Event.dt_arr property.
    """

    pass

def calc_pos_arr():
    """
    Using .json linear fit file, converts dt array to position array.

    Args:

    Returns:
        None
        => Creates or updates Event.pos_arr property. 
    """

    pass
