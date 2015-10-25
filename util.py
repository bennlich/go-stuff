import os
import numpy as np

def directory_map(dir, fn):
    '''
    Applies fn to every file path in dir.
    Returns a list of results.

    '''
    results = []
    for root, dirs, files in os.walk(dir):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            results.append(fn(os.path.join(root, file)))

    return results

def pad_hist(counts, target_length):
    '''
    Pad *counts* with 0s so its length becomes target_length.

    '''
    new_counts = np.zeros(target_length)
    new_counts[:counts.size] = counts
    return new_counts
