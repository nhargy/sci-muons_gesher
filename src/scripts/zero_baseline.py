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
pdf_path = os.path.join(out_path, 'zero_baseline.pdf')

# Initialise pdf
pdf      = PdfPages(pdf_path)

# Define path to specific run
dir_path = 'Calib/Position'
run_path = os.path.join(lcd_path, dir_path)

# Define scope config
scope_config = [('dt-run8',4)] #,('scope-2-run4',4)]

# Choose segment
segment = sys.argv[1]

# Initialise event object
myevent = Event(run_path, segment, scope_config)

# Process event data and store in variables
myevent.get_data()
mydata = myevent.data
times  = myevent.times

# ======================
# Plot uncorrected data
# ======================

fig, axs = plt.subplots(nrows=2, ncols=2, figsize = (8,6), sharex=True, sharey=True)

#axs[0][0].set_ylim(-250,1500)
axs[0][0].set_xlim(0,100)

# Plot grey line at zero
for row in axs:
    for col in row:
        col.axhline(0, linewidth=5, alpha=0.4, color='grey')

# Plate 1
axs[0][0].plot(times[0], mydata[0], label = 'scope1-ch1')
axs[0][0].plot(times[0], mydata[1], label = 'scope1-ch2')
axs[0][0].set_title('Plate 1')
axs[0][0].legend()

# Plate 2
axs[0][1].plot(times[0], mydata[2], label = 'scope1-ch3')
axs[0][1].plot(times[0], mydata[3], label = 'scope1-ch4')
axs[0][1].set_title('Plate 2')
axs[0][1].legend()

try:
    # Plate 3
    axs[1][0].plot(times[1], mydata[4], label = 'scope2-ch1')
    axs[1][0].plot(times[1], mydata[5], label = 'scope2-ch2')
    axs[1][0].set_title('Plate 3')
    axs[1][0].legend()

    # Plate 4
    axs[1][1].plot(times[1], mydata[6], label = 'scope2-ch3')
    axs[1][1].plot(times[1], mydata[7], label = 'scope2=ch4')
    axs[1][1].set_title('Plate 4')
    axs[1][1].legend()

except:
    print("Probably only 2 plates!")

fontsize = 18
fig.supxlabel("Time [ns]", fontsize=fontsize)
fig.supylabel("Voltage [mV]", fontsize=fontsize)

fig.suptitle(f'{dir_path}, segment: {segment}', fontsize=fontsize)

fig.tight_layout()

# Send to pdf
pdf.savefig()
plt.close()

# =============================
# Plot baseline-corrected data
# =============================

mydata2  = [] # baseline corrected mydata
unmasked = [] # Only the unmasked part, i.e. the baseline
for wf in mydata:
    bl, std, wf_smooth, mask = fn.find_baseline(wf)
    wf2 = wf - bl
    unm = np.ma.array(wf2, mask=mask)

    mydata2.append(wf2)
    unmasked.append(unm)


fig, axs = plt.subplots(nrows=2, ncols=2, figsize = (8,6), sharex=True, sharey=True)

# Plot grey line at zero
for row in axs:
    for col in row:
        col.axhline(0, linewidth=5, alpha=0.4, color='grey')
        col.axhline(120, linewidth=2.5, alpha=0.5, color='red', linestyle='--')

#axs[0][0].set_ylim(-250,1500)
axs[0][0].set_xlim(0,100)
unm_col = 'green'

# Plate 1
axs[0][0].plot(times[0], mydata2[0], label = 'scope1-ch1')
axs[0][0].plot(times[0], mydata2[1], label = 'scope1-ch2')

axs[0][0].plot(times[0], unmasked[0], color=unm_col, label = 'Baseline')
axs[0][0].plot(times[0], unmasked[1], color=unm_col)
axs[0][0].legend()

# Plate 2
axs[0][1].plot(times[0], mydata2[2], label = 'scope1-ch3')
axs[0][1].plot(times[0], mydata2[3], label = 'scope1-ch4')

axs[0][1].plot(times[0], unmasked[2], color=unm_col, label = 'Baseline')
axs[0][1].plot(times[0], unmasked[3], color=unm_col)
axs[0][1].legend()

try:
    # Plate 3
    axs[1][0].plot(times[1], mydata2[4], label = 'scope2-ch1')
    axs[1][0].plot(times[1], mydata2[5], label = 'scope2-ch2')
    
    axs[1][0].plot(times[1], unmasked[4], color=unm_col, label = 'Baseline')
    axs[1][0].plot(times[1], unmasked[5], color=unm_col)
    axs[1][0].legend()
    
    # Plate 4
    axs[1][1].plot(times[1], mydata2[6], label = 'scope2-ch3')
    axs[1][1].plot(times[1], mydata2[7], label = 'scope2-ch4')
    
    axs[1][1].plot(times[1], unmasked[6], color=unm_col, label='Baseline')
    axs[1][1].plot(times[1], unmasked[7], color=unm_col)
    axs[1][1].legend()

except:
    print("Probably only 2 plates")

fig.supxlabel("Time [ns]", fontsize=fontsize)
fig.supylabel("Voltage [mV]", fontsize=fontsize)


fig.suptitle(f"Baseline-corrected; {dir_path}, segment: {segment}", fontsize=fontsize)
fig.tight_layout()

pdf.savefig()
plt.close()

# ======================= #
# END OF SCRIPT PROTOCOLS #
# ======================= #

# End script with closing of pdf
pdf.close()
