# Importing Libs
import numpy as np
import soundfile as sf
import scipy.signal as sg
from scipy.interpolate import interp1d


def interpolate_matrix(matrix):
    n_rows, n_cols = matrix.shape
    interpolated_matrix = np.zeros((n_rows, 1000))

    for i in range(n_rows):
        # Cria pontos de referência na escala 0-1
        x = np.linspace(0, 1, n_cols)
        y = matrix[i]  # Valores da linha atual

        # Cria a função de interpolação
        f = interp1d(x, y, kind='cubic')

        # Interpola os valores em uma nova escala de 0-1 com 1000 pontos
        interpolated_values = f(np.linspace(0, 1, 1000))

        interpolated_matrix[i] = interpolated_values

    return interpolated_matrix


def moving_average_filter(signal, N):
    # Creating our moving average filter with N terms
    _filter = np.ones(N) / N

    # Performing convolution of the signal with the filter, which returns a filtered signal
    signal_filtered = np.convolve(signal, _filter, mode='full')

    # Since the resulting signal from convolution introduces a delay, we need to adjust it
    return signal_filtered[(N-1):len(signal_filtered)]

# Get the duration in seconds


def get_duration_audio(file):
    with sf.SoundFile(file) as f:
        duration = len(f) / f.samplerate
    return int(duration)


def format_date_str(date_str):
    year = date_str[0:4]
    month = date_str[4:6]
    day = date_str[6:8]
    return f"{day}/{month}/{year}"
