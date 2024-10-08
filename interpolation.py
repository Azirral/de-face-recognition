import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd
import csv
#%%

# Original data
file_path = 'C:/Users/oskik/PycharmProjects/InżynierkaSandbox/S01_wristband/C01/HR.csv'

# Read the CSV file, skipping the first row, selecting only the second column, and not using any row as header
df = pd.read_csv(file_path, header=None, skiprows=2)
original_time = np.arange(len(df))
# Convert the DataFrame column to a NumPy ndarray
heart_rate = df.to_numpy().flatten()

#%%

# New time array for 4 Hz sampling rate
new_time = np.arange(0, len(heart_rate) - 1 + 0.25, 0.25)
print(len(heart_rate))
print(len(original_time))
print(len(new_time))
#%%

# Cubic interpolation
interpolator = interp1d(original_time, heart_rate, kind='cubic')
new_heart_rate = interpolator(new_time)

plt.plot(original_time, heart_rate, 'o', label='Original data (1 Hz)')
plt.plot(new_time, new_heart_rate, '-', label='Interpolated data (4 Hz)')
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Heart Rate')
plt.show()