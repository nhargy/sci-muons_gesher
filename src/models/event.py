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
                    wf      = fn.get_waveform(csvfile)
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


