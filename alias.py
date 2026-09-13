"""Undersøk aliasing i et firkantsignal ved ulike samplingfrekvenser."""

import numpy as np

from signalverktoy import (
    aliasfrekvens,
    plott_tid_og_spekter,
    syntetiser_firkantsignal,
)


SAMPLINGSFREKVENSER = [5000, 2500, 1200, 1000]
ANTALL_HARMONISKE = 10


def main() -> None:
    for fs in SAMPLINGSFREKVENSER:
        signal, tid, harmoniske, _ = syntetiser_firkantsignal(
            ANTALL_HARMONISKE,
            fs,
            dur=0.02,
        )
        plott_tid_og_spekter(
            signal,
            tid,
            fs,
            f"Firkantsignal: N = {ANTALL_HARMONISKE}, fs = {fs} Hz",
            tidsvindu_ms=8,
        )

        under = harmoniske[harmoniske < fs / 2]
        paa_nyquist = harmoniske[np.isclose(harmoniske, fs / 2)]
        over = harmoniske[harmoniske > fs / 2]
        aliaser = [aliasfrekvens(frekvens, fs) for frekvens in over]

        print(f"fs = {fs} Hz")
        print("  Under Nyquist:", under.tolist())
        print("  På Nyquist:", paa_nyquist.tolist())
        print("  Over Nyquist:", over.tolist())
        print("  Aliasfrekvenser:", aliaser)


if __name__ == "__main__":
    main()
