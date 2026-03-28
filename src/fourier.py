import numpy as np

def coeffs(points, n_coeffs):
    coefficients = np.fft.fft(points, norm="forward")
    freqs = np.fft.fftfreq(len(points), 1 / len(points))

    dc = np.where(freqs == 0)[0]
    ac = np.where(freqs != 0)[0]
    order = np.argsort(-np.abs(coefficients[ac]))
    ac = ac[order[:n_coeffs - len(dc)]]
    keep = np.concatenate([dc, ac])

    freqs = freqs[keep]
    coefficients = coefficients[keep]
    amps = np.abs(coefficients)
    phases = np.angle(coefficients)

    return amps, freqs, phases 