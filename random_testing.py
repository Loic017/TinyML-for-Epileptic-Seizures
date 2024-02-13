import numpy as np
import os
import pandas
import mne
import matplotlib.pyplot as plt

DEV_DATA_FOLDER = r"seizure_dataset\edf_resampled\dev"
TRAIN_DATA_FOLDER = r"seizure_dataset\edf_resampled\train"

TEST_FILE = (
    DEV_DATA_FOLDER + r"\01_tcp_ar\002\00000258\s003_2003_07_22\00000258_s003_t002.edf"
)

raw = mne.io.read_raw_edf(TEST_FILE)

# raw.compute_psd().plot()
raw.load_data()
raw.plot(duration=50, n_channels=32)
