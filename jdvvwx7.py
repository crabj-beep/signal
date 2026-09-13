"""Referansemåling med signalets tre frekvenskomponenter."""

import numpy as np

from signalverktoy import plott_tid_og_spekter, syn_sin


FREKVENSER = np.array([100, 700, 1100], dtype=float)
AMPLITUDER = np.array([2.0, 1.0, 0.5], dtype=float)
FASER = np.array([np.pi / 4, 0, -np.pi / 2])
KOMPLEKSE_AMPLITUDER = AMPLITUDER * np.exp(1j * FASER)

REFERANSE_FS = 5000
MAALETID = 0.05


def lag_referansesignal(fs: float = REFERANSE_FS, dur: float = MAALETID):
    """Generer signalet fra oppgaven med ønsket samplingsfrekvens."""
    return syn_sin(FREKVENSER, KOMPLEKSE_AMPLITUDER, fs, dur)


def main() -> None:
    signal, tid = lag_referansesignal()
    frekvens, amplitude = plott_tid_og_spekter(
        signal,
        tid,
        REFERANSE_FS,
        "Referansemåling: fs = 5000 Hz",
    )

    print(f"Antall sampler: {len(signal)}")
    print(f"Frekvensoppløsning: {frekvens[1] - frekvens[0]:.1f} Hz")

    for forventet in FREKVENSER:
        indeks = np.argmin(np.abs(frekvens - forventet))
        print(
            f"{forventet:4.0f} Hz -> målt amplitude "
            f"{amplitude[indeks]:.3f} V"
        )


if __name__ == "__main__":
    main()
