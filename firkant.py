"""Vis hvordan 3, 5 og 10 harmoniske bygger opp et firkantsignal."""

import matplotlib.pyplot as plt

from signalverktoy import plott_tid_og_spekter, syntetiser_firkantsignal


REFERANSE_FS = 50_000
VARIGHET = 0.01


def main() -> None:
    figur, akser = plt.subplots(3, 1, figsize=(10, 8), sharex=True, sharey=True)

    for akse, antall_harmoniske in zip(akser, [3, 5, 10]):
        signal, tid, _, _ = syntetiser_firkantsignal(
            antall_harmoniske,
            REFERANSE_FS,
            VARIGHET,
        )
        utsnitt = tid * 1000 <= 4
        akse.plot(tid[utsnitt] * 1000, signal[utsnitt])
        akse.axhline(1, color="grey", ls="--", lw=1)
        akse.axhline(-1, color="grey", ls="--", lw=1)
        akse.set_title(f"N = {antall_harmoniske} harmoniske")
        akse.set_ylabel("Amplitude [V]")

    akser[-1].set_xlabel("Tid [ms]")
    figur.suptitle("Firkantsignal med økende antall harmoniske")
    figur.tight_layout()
    plt.show()

    signal, tid, harmoniske, amplituder = syntetiser_firkantsignal(
        10,
        REFERANSE_FS,
        VARIGHET,
    )
    plott_tid_og_spekter(
        signal,
        tid,
        REFERANSE_FS,
        "Firkantsignal med N = 10",
        tidsvindu_ms=4,
    )

    print("Forventede harmoniske og amplituder:")
    for frekvens, amplitude in zip(harmoniske, amplituder):
        print(f"{frekvens:5.0f} Hz : {amplitude:.4f} V")


if __name__ == "__main__":
    main()
