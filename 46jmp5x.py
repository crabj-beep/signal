"""Sammenligning av np.fft.fft og np.fft.rfft."""

import matplotlib.pyplot as plt
import numpy as np

from referansemaaling import REFERANSE_FS, lag_referansesignal


def main() -> None:
    signal, _ = lag_referansesignal()
    signal = signal - np.mean(signal)
    antall_sampler = len(signal)

    transform_full = np.fft.fft(signal)
    frekvens_full = np.fft.fftfreq(antall_sampler, d=1 / REFERANSE_FS)
    amplitude_full = np.abs(transform_full) / antall_sampler

    transform_real = np.fft.rfft(signal)
    frekvens_real = np.fft.rfftfreq(antall_sampler, d=1 / REFERANSE_FS)
    amplitude_real = 2 * np.abs(transform_real) / antall_sampler
    amplitude_real[0] /= 2
    if antall_sampler % 2 == 0:
        amplitude_real[-1] /= 2

    figur, akser = plt.subplots(1, 2, figsize=(12, 4))

    akser[0].stem(frekvens_full, amplitude_full, basefmt=" ")
    akser[0].set_xlim(-1500, 1500)
    akser[0].set_title("fft: positivt og negativt spekter")
    akser[0].set_xlabel("Frekvens [Hz]")
    akser[0].set_ylabel("Tosidig amplitude [V]")

    akser[1].stem(frekvens_real, amplitude_real, basefmt=" ")
    akser[1].set_xlim(0, 1500)
    akser[1].set_title("rfft: enkeltsidig spekter")
    akser[1].set_xlabel("Frekvens [Hz]")
    akser[1].set_ylabel("Enkeltsidig amplitude [V]")

    figur.tight_layout()
    plt.show()

    print("fft viser både positive og negative frekvenser.")
    print("rfft viser bare frekvensene fra 0 Hz til Nyquist.")


if __name__ == "__main__":
    main()
