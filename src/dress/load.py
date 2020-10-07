"""

"""

# Other imports
import h5py
import numpy as np
from shutil import copyfile
from os.path import join


def _load_entry(file_handle, entry=None):
    """
    Read events inside given file.
    """

    events = {}
    events["tof"] = np.array(file_handle[join(entry, "event_time_offset")][()],
                             dtype=np.float64) / 1.0e3
    events["ids"] = np.array(file_handle[join(entry, "event_id")][()])
    events["index"] = np.array(file_handle[join(entry, "event_index")][()])
    return events


def load(filename, entries=None):
    """
    Load events in a file.
    """

    # Automatically find event entries if not specified
    if entries is None:
        entries = []
        key = "event_time_offset"
        with h5py.File(filename, "r") as infile:
            contents = []
            infile.visit(contents.append)
        for item in contents:
            if item.endswith(key):
                entries.append(item.replace(key, ""))

    data = {}
    with h5py.File(filename, "r") as infile:
        for e in entries:
            data[e] = _load_entry(file_handle=infile, entry=e)

    return data
