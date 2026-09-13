"""Aliasing av signalet med komponenter på 100, 700 og 1100 Hz."""

from referansemaaling import (
    FREKVENSER,
    KOMPLEKSE_AMPLITUDER,
    MAALETID,
)
from signalverktoy import aliasfrekvens, plott_tid_og_spekter, syn_sin


SAMPLINGSFREKVENSER = [5000, 2500, 1600, 1200, 1100]


def main() -> None:
    for fs in SAMPLINGSFREKVENSER:
        signal, tid = syn_sin(
            FREKVENSER,
            KOMPLEKSE_AMPLITUDER,
            fs,
            MAALETID,
        )
        plott_tid_og_spekter(
            signal,
            tid,
            fs,
            f"Sammensatt signal: fs = {fs} Hz",
        )

        aliaser = [aliasfrekvens(frekvens, fs) for frekvens in FREKVENSER]
        print(
            f"fs={fs:4d} Hz, Nyquist={fs/2:6.0f} Hz, "
            f"forventede frekvenser={aliaser}"
        )


if __name__ == "__main__":
    main()
