import numpy as np
import csv

def get_timestamps(filepath, segments = 1000):
    """
    Reads the <filename>_info.txt files generated by IF_bin_to_csv.py script
    and extracts an array of timestamps.

    Args:
        filepath (str) : path to <filename>_info.txt file
                         example filename: 'scope-1-run7_info.txt'
        segments (int) : the total number of segments in a run (1000 is max for 
                         our scope)
    Returns:
        timestamps (ndarray) : numpy array of floats in seconds
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Initialise empty timestamps numpy array, expect floats
        timestamps = np.empty(segments, dtype=float)
        count      = 0

        # Loop through all the lines in the file to find 'Time Tags'
        for line in lines:
            if count >= segments:
                break
            if 'Time Tags' in line:
                timestamp = line.split(" = ")[-1]
                timestamp = float(timestamp.split('\'')[1])
                timestamps[count] = timestamp
                count += 1

        # Cut the timestamps array if there are less events than
        # expected segments
        if count < segments:
            timestamps = timestamps[:count]

        return timestamps

    except Exception as e:
        print("Error in 'get_timestamps'")
        print(e)
        return None


def get_waveform(csvfile):
    """
    Extracts the x,y data from the csv waveform file.

    Args:
        csvfile (str)  : path to csv file containing waveform
                         example filename: scope-1-run3_segment-1_1.csv

    Returns:
        data (ndarray) : two dimensional numpy array containt x and y
                         subarrays
    """
    try:
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            data   = np.array(list(reader), dtype=float)
            data   = data.T
        return data

    except Exception as e:
        print("Error in get_waveform")
        print(e)
        return None
