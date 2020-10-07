"""

"""

# Dress imports
from ..load import load
from . import v20
from .wfm import get_frames
from .stitch_events import stitch_events

# Other imports
import h5py
import numpy as np
from shutil import copyfile
from os.path import join


def _stitch_file(file_handle, entry=None, frames=None, plot=False):
    """
    Read events inside given file, and stitch events according to frames.
    """

    # Get time offsets from file
    events = {}
    events["tof"] = np.array(file_handle[entry + "event_time_offset"][...],
                             dtype=np.float64,
                             copy=True) / 1.0e3

    # Get the data from nexus file
    events["ids"] = np.array(file_handle[entry + "event_id"][...],
                             dtype=np.uint32,
                             copy=True)
    events["index"] = np.array(file_handle[entry + "event_index"][...],
                               dtype=np.uint64,
                               copy=True)

    # Stitch the data
    stitched = stitch_events(events=events, frames=frames, plot=plot)

    # Update event_index entry
    file_handle[entry + "event_index"][...] = stitched["index"]
    # Delete old event_id and event_time_offset
    del file_handle[entry + "event_id"]
    del file_handle[entry + "event_index"]
    del file_handle[entry + "event_time_offset"]
    # Create new event_id and event_time_offset
    event_id_ds = file_handle[entry].create_dataset('event_id',
                                                    stitched["ids"].shape,
                                                    data=stitched["ids"],
                                                    compression='gzip',
                                                    compression_opts=1)
    event_index_ds = file_handle[entry].create_dataset('event_index',
                                                       stitched["index"].shape,
                                                       data=stitched["index"],
                                                       compression='gzip',
                                                       compression_opts=1)
    event_offset_ds = file_handle[entry].create_dataset(
        'event_time_offset',
        stitched["tof"].shape,
        data=np.array(stitched["tof"] * 1.0e3, dtype=np.uint32),
        compression='gzip',
        compression_opts=1)
    event_offset_ds.attrs.create('units', np.array('ns').astype('|S2'))

    return


def stitch_files(files=None, entries=None, plot=False, frames=None):

    if isinstance(files, str):
        files = files.split(",")
    elif not isinstance(files, list):
        files = [files]

    v20setup = v20.setup()
    v20frames = get_frames(instrument=v20setup)

    for f in files:

        print("\nProcessing file:", f)

        ext = ".{}".format(f.split(".")[-1])
        outfile = f.replace(ext, "_stitched" + ext)

        copyfile(f, outfile)

        # Automatically find event entries if not specified
        if entries is None:
            entries_ = []
            key = "event_time_offset"
            with h5py.File(outfile, "r") as f:
                contents = []
                f.visit(contents.append)
            for item in contents:
                if item.endswith(key):
                    entries_.append(item.replace(key, ""))
        else:
            entries_ = entries.split(",")

        # Loop through entries and shift event tofs
        with h5py.File(outfile, "r+") as outf:

            # Compute WFM frame shifts and boundaries from V20 setup
            if frames is None:
                v20setup = v20.setup(filename=outf)
                # v20setup = v20.setup()
                v20frames = get_frames(instrument=v20setup)

            for e in entries_:
                print("==================")
                print("Entry:", e)
                this_plot = plot
                if plot is True:
                    this_plot = (outfile + "-" + e + ".pdf").replace("/", "_")

                if e.count("monitor") > 0:
                    frames = v20frames["monitor"]
                else:
                    frames = v20frames["DENEX"]

                _stitch_file(file_handle=outf,
                             entry=e,
                             frames=frames,
                             plot=this_plot)
