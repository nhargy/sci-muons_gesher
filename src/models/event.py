import os
import sys
import numpy as np

# Get current working directory
cwd        = os.getcwd()

# Relative path of sci-muons_gesher/src
repo_path  = cwd.split('/src')[0]

# Path to utils
utils_path = os.path.join(repo_path, 'src/utils')

# Add utils path to system
sys.path.insert(0, utils_path)

try:
    import functions as fn
except:
    print('Failure to import utils/functions. Check whether system path is correct:')
    print(utils_path)


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
        <Description>

        Args:

        Returns:

        """
        data = []
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

        #data      = np.array(data)
        self.data = data

        return data
