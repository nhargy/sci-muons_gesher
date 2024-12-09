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

# Define important paths
repo_path = cwd.split('/src')[0]
lcd_path  = os.path.join(repo_path, 'lcd')
out_path  = os.path.join(repo_path, 'out')
plt_path  = os.path.join(repo_path, 'plt')


# =================================
# Plot example event onto live pdf
# =================================
"""
In the following example we will load an event and plot its data
onto a note pdf file.
"""

# Define path to pdf
pdf_path      = os.path.join(out_path, 'example1.pdf')

# Initialise pdf
pdf           = PdfPages(pdf_path)

# Define path to specific run
dir_path      = 'VS1/Run5'
vs1_run4_path = os.path.join(lcd_path, dir_path)

# Define scope_config
scope_config  = [('scope-1-run5', 4),('scope-2-run5', 4)]
"""
scope_config: each tuple specifies the scope name as given in the saved csv files
              and the corresponding number of active channels. 
"""

# Choose segment
segment       = 100

# Define event object
myevent       = Event(vs1_run4_path, segment, scope_config)

# Process event data and store in variable
myevent.get_data()
mydata = myevent.data     # waveform matrix of all channels
times  = myevent.times    # the x-axis time values, one array for each scope

# Plot
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(times[0], mydata[0], label='Ch1')
ax.plot(times[0], mydata[1], label='Ch2')
ax.set_title(f'{dir_path}; Segment {segment}')
ax.set_xlabel('Time [seconds]')
ax.set_ylabel('Volts')
fig.legend()

# Format for pdf view
fig.tight_layout()

# Save to pdf object
pdf.savefig()
plt.close()

# End script in closing pdf object so it can refresh
pdf.close()
