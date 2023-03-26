import numpy as np
from lalinference import BurstSineGaussianF


def sine_gaussian_frequency(
    frequency_array: np.ndarray,
    hrss: float,
    quality: float,
    frequency: float,
    phase: float,
    eccentricity: float,
    **kwargs,
):

    """
    Frequency domain sine gaussian built on top of
    lalinference BurstSineGaussianF.
    Meant to be used in conjunction with bilby WaveformGenerator
    Args:
        frequency_array: frequencies at which to evaluate model
        hrss: amplitude
        q: quality factor
        frequency: central frequency of waveform
        phase: phase of waveform
        eccentricity: relative fraction of hplus / hcross

    """

    # number of frequencies
    n_freqs = len(frequency_array)

    # infer df from frequency array
    df = frequency_array[1] - frequency_array[0]

    # infer dt from nyquist
    dt = 1 / (2 * frequency_array[-1])

    # calculate hplus and hcross from lalinference
    hplus, hcross = BurstSineGaussianF(
        quality, frequency, hrss, eccentricity, phase, df, dt
    )
    plus = np.zeros(n_freqs, dtype=complex)
    cross = np.zeros(n_freqs, dtype=complex)

    plus[: len(hplus.data.data)] = hplus.data.data
    cross[: len(hcross.data.data)] = hcross.data.data

    return dict(plus=plus, cross=cross)
