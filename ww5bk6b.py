"""Felles funksjoner for PHYS116 lab 1."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def sett_plotstil() -> None:
    """Bruk en tydelig og konsekvent stil på figurene."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({"figure.figsize": (10, 4), "font.size": 11})


def syn_sin(fk, Xk, fs: float, dur: float, tstart: float = 0.0):
    """Syntetiser et reelt signal fra frekvenser og komplekse amplituder."""
    fk = np.asarray(fk, dtype=float)
    Xk = np.asarray(Xk, dtype=complex)

    antall_sampler = int(round(fs * dur))
    tid = tstart + np.arange(antall_sampler) / fs

    amplituder = np.abs(Xk)[:, None]
    faser = np.angle(Xk)[:, None]
    frekvenser = fk[:, None]

    signal = np.sum(
        amplituder * np.cos(2 * np.pi * frekvenser * tid + faser),
        axis=0,
    )
    return signal, tid


def amplitude_spectrum(signal, fs: float):
    """Beregn frekvensakse og normalisert enkeltsidig amplitudespekter."""
    signal = np.asarray(signal, dtype=float)
    signal = signal - np.mean(signal)

    antall_sampler = len(signal)
    transform = np.fft.rfft(signal)
    frekvens = np.fft.rfftfreq(antall_sampler, d=1 / fs)

    amplitude = 2 * np.abs(transform) / antall_sampler
    amplitude[0] /= 2
    if antall_sampler % 2 == 0:
        amplitude[-1] /= 2

    return frekvens, amplitude


def aliasfrekvens(frekvens: float, fs: float) -> float:
    """Returner observert frekvens mellom 0 og Nyquist-frekvensen."""
    foldet = (frekvens + fs / 2) % fs - fs / 2
    return float(abs(foldet))


def plott_tid_og_spekter(
    signal,
    tid,
    fs: float,
    tittel: str,
    tidsvindu_ms: float = 20,
):
    """Vis et kort tidsutsnitt og det enkeltsidige amplitudespekteret."""
    frekvens, amplitude = amplitude_spectrum(signal, fs)
    nyquist = fs / 2

    figur, akser = plt.subplots(1, 2, figsize=(12, 4))

    utsnitt = tid * 1000 <= tidsvindu_ms
    akser[0].plot(tid[utsnitt] * 1000, signal[utsnitt], lw=1.4)
    akser[0].set_xlabel("Tid [ms]")
    akser[0].set_ylabel("Amplitude [V]")
    akser[0].set_title("Tidsdomene")

    akser[1].stem(frekvens, amplitude, basefmt=" ")
    akser[1].axvline(
        nyquist,
        color="crimson",
        ls="--",
        lw=1.4,
        label=f"Nyquist = {nyquist:g} Hz",
    )
    akser[1].set_xlim(0, nyquist)
    akser[1].set_xlabel("Frekvens [Hz]")
    akser[1].set_ylabel("Amplitude [V]")
    akser[1].set_title("Frekvensdomene")
    akser[1].legend()

    figur.suptitle(tittel)
    figur.tight_layout()
    plt.show()
    return frekvens, amplitude


def syntetiser_firkantsignal(
    antall_harmoniske: int,
    fs: float,
    dur: float,
    f0: float = 500,
    A: float = 1.0,
):
    """Tilnærm et symmetrisk firkantsignal med odde harmoniske."""
    indeks = np.arange(1, antall_harmoniske + 1)
    oddetall = 2 * indeks - 1

    harmoniske = oddetall * f0
    amplituder = 4 * A / (np.pi * oddetall)
    faser = np.full(antall_harmoniske, -np.pi / 2)
    komplekse_amplituder = amplituder * np.exp(1j * faser)

    signal, tid = syn_sin(harmoniske, komplekse_amplituder, fs, dur)
    return signal, tid, harmoniske, amplituder


sett_plotstil()
