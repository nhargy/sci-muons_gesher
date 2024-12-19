import os
import sys
import numpy as np
import json
from scipy.interpolate import interp1d

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


class Event:
    """
    Event object containig all measured data and metadata from a 
    triggered scope event, together with derived values and properties.
    """
    def __init__(self, dirpath, segment, scope_config):
        """
        Args:
            dirpath (str)          : path to directory containing the data csv files
            segment (int)          : the desired trigger event from the measurement run
            scope_config (ndarray) : a 1D array of tuples. The first element of the tuple
                                     contains the scope name and the run number, while
                                     the second element contains the associated number of
                                     channels for that scope.
                                     Example: [('scope-1-run8', 4),('scope-2-run8', 4)].
        """
        self.dirpath      = dirpath
        self.segment      = segment
        self.scope_config = scope_config

        self.risetime_matrix = None
        self.dt_arr          = None
        self.x_arr           = None

        # Structure risetime and dt matrices
        self.struct_risetime_matrix()

    def struct_risetime_matrix(self):
        """
        Given self.scope_config, this function create an np.nan numpy matrix
        in the shape of the experiment. For example, scope_config = [('scope-1', 4),('scope-2',4)]
        means that there are two scopes with 4 channels each, which in turn means two scintillator
        plates per scope. The matrix shape will then be ((4, 2)).

        Args:
            None
        Returns:
            None
            => Updates self.risetime_mtx.
        """
        if len(self.scope_config) == 2:
            matrix = [[],[]]
        elif len(self.scope_config) == 1:
            matrix = [[]]

        dt_len = 0

        for num, scope in enumerate(matrix):
            ch_num = self.scope_config[num][1]
            plate_num = int(ch_num/2)
            for plate in range(plate_num):
                matrix[num].append([np.nan, np.nan])
                dt_len += 1

        risetime_matrix = np.array(matrix)
        dt_arr       = np.empty(dt_len)
        dt_arr[:]    = np.nan

        self.risetime_matrix = risetime_matrix
        self.dt_arr       = dt_arr


    def get_data(self):
        """
        Extracts the waveforms and time data from a given triggered event, or segment.
        The function adds self.data and self.time attributes to the event object.

        Args:
            None
        Returns:
            None
        """
        data  = [] # store waveform matrix
        times = [] # store time axis for each scope as they can be different
        for scope in self.scope_config:
            for ch in range(1, scope[1]+1):
                try:
                    csvfile = os.path.join(self.dirpath, f'{scope[0]}_segment-{self.segment}_{ch}.csv')
                    wf      = fn.get_waveform(csvfile, yconv=1e3)
                except Exception as e:
                    print('Failed to get waveform from csv file. Error:')
                    print(e)
                    wf      = [np.nan]
                data.append(wf)

            wf = fn.get_waveform(csvfile, xignore=False, xconv=1e9)
            t  = wf[0]
            times.append(t)

        self.data  = data
        self.times = times


    def zero_baselines(self):
        """
        <Decription>

        Args:

        Returns:

        """
        for num, row in enumerate(self.data):
            bl = fn.find_baseline(row)[0]
            wf = row - bl
            self.data[num] = wf


    def calc_risetime_mtx(self, ROI, threshold, fraction): # would all be self.<property>
        """
        Calculates the risetime of each peak on each scintillator plate, if it exists.

        Args:
            
        Returns:
            None
            => Updates self.risetime_mtx and self.dt_arr property.
        """
        dt_meta = []
        wf_idx = 0
        for scope_idx, scope in enumerate(self.risetime_matrix):
            t = self.times[scope_idx]
            a = np.argmin(np.abs(t - ROI[0]))
            b = np.argmin(np.abs(t - ROI[1]))
            ROI_idx = (a,b)
            print(ROI_idx)
            for plate_idx, plate in enumerate(scope):
                wf1 = self.data[wf_idx]
                wf2 = self.data[wf_idx+1]

                p1, _ = fn.get_first_peak(wf1, threshold=threshold, ROI=ROI_idx)
                p2, _ = fn.get_first_peak(wf2, threshold=threshold, ROI=ROI_idx)



                if p1 and p2 != None:
                    fraction  = fraction
                    rt1 = fn.get_risetime(t, wf1, p1, ROI, fraction=fraction)
                    rt2 = fn.get_risetime(t, wf2, p2, ROI, fraction=fraction)

                    self.risetime_matrix[scope_idx][plate_idx][0] = rt1
                    self.risetime_matrix[scope_idx][plate_idx][1] = rt2

                    tup1 = (p1, rt1)
                    tup2 = (p2, rt2)

                    dt = rt1 - rt2
                    self.dt_arr[int(wf_idx/2)] = dt
                    dt_meta.append([tup1, tup2])
                else:
                    tup_nan = (np.nan, np.nan)
                    dt_meta.append([tup_nan, tup_nan])

                wf_idx += 2
        
        self.dt_meta = dt_meta


    def calc_pos_arr(self, filepath, x_min=0, x_max=144, max_err=25):
        """
        Using .json linear fit file, converts dt array to position array.

        Args:

        Returns:
            None
            => Creates or updates Event.pos_arr property. 
        """
        with open(filepath, 'r') as f:
            popt = json.load(f)['popt']
            #popt    = content['popt']
        
        # Linear function
        def linear(x, m, c):
            return m*x + c

        # Generate linear array
        x_vals = np.linspace(-100,244)
        y_vals = linear(x_vals, *popt)

        f_inv = interp1d(y_vals, x_vals, kind='linear')

        # Create the position array
        x_arr = np.empty(len(self.dt_arr))
        x_arr[:] = np.nan

        for idx, dt in enumerate(self.dt_arr):
            x = f_inv(dt)
            if (x >= x_min) and (x <= x_max):
                x_arr[idx] = x
            elif (x < x_min) and (x > x_min - max_err):
                x_arr[idx] = x_min
            elif (x > x_max) and (x < x_max + max_err):
                x_arr[idx] = x_max

        self.x_arr = x_arr

