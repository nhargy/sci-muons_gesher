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


class Event:
    """
    Event object of the waveform measured from one triggered event
    on multiple scopes.
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

        # Structure risetime and dt matrices
        self.struct_risetime_mtx()

    def struct_risetime_mtx(self):
        """
        Given self.scope_config, this function create an np.nan numpy matrix
        in the shape of the experiment. For example, scope_config = [('scope-1', 4),('scope-2',4)]
        means that there are two scopes with 4 channels each, which in turn means two scintillator
        plates per scope. The matrix shape will then be ((4, 2)).

        Args:
            None
        Returns:
            None
            => Creates or upates self.risetime_mtx.
        """
        if len(self.scope_config) == 2:
            mtx = [[],[]]
        elif len(self.scope_config) == 1:
            mtx = [[]]

        dt_len = 0

        for num, scope in enumerate(mtx):
            ch_num = self.scope_config[num][1]
            plate_num = int(ch_num/2)
            for plate in range(plate_num):
                mtx[num].append([np.nan, np.nan])
                dt_len += 1

        risetime_mtx = np.array(mtx)
        dt_arr       = np.empty(dt_len)
        dt_arr[:]    = np.nan

        self.risetime_mtx = risetime_mtx
        self.dt_arr       = dt_arr

        return None


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

        return None


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
        return None

