import numpy as np
import matplotlib.pyplot as plt


# henter def for bølgen fra pre lab opptavetekst
def syn_sin(fk, Xk, fs, dur, tstart=0.0):
    fk = np.asarray(fk, dtype=float)
    Xk = np.asarray(Xk, dtype=complex)
    N = int(round(fs * dur))
    tt = tstart + np.arange(N) / fs
    amplitudes = np.abs(Xk)[:, None]
    phases = np.angle(Xk)[:, None]
    frequencies = fk[:, None]
    xx = np.sum(
    amplitudes
    * np.cos(2 * np.pi * frequencies * tt + phases),
    axis=0,
    )
    return xx, tt

# setter først opp det som trengs for å generer det syntetiske signalet

fk = np.array([100,700,1100], dtype=float) #signales tre frekvers
ak = np.array([2.0,1.0,0.5], dtype=float) #signales tre amplituder
phik = np.array([np.pi / 4, 0, -np.pi / 2], dtype=float) #signales tre faser
xk = ak * np.exp(1j * phik) #signales tre komplekse koeffisienter 

fs = 5000 #samplingsfrekvens
dur = 0.05

# lager så signalet
signal, t = syn_sin(fk, xk, fs, dur)


# Generer signalet (henter inn verdi og tidskoordianter)
signal, t = syn_sin(fk, xk, fs, dur)


# Tidsplott
utsnitt = t <= 0.03 # her så er det nok til å se 3 perioder

plt.figure(figsize=(10, 4))
plt.plot(t[utsnitt] * 1000, signal[utsnitt])
plt.xlabel("Tid [ms]")
plt.ylabel("Amplitude [V]")
plt.title("Sammensatt signal")
plt.grid()
plt.tight_layout()
plt.show()


'''def amplitude_spectrum(signal, fs):
    signal = np.asarray(signal, dtype=float)
    signal = signal - np.mean(signal)
    N = len(signal)
    X = beregn fft og rfft
    freq = lag frekvensakse
    amplitude = normaliser enkeltsidig spekter
    return freq, amplitude'''


def amplitude_spectrum(signal, fs):
    signal = np.asarray(signal, dtype=float)
    signal = signal - np.mean(signal)

    N = len(signal)

    X = np.fft.rfft(signal) # regner ut fft og rfft
    freq = np.fft.rfftfreq(N, d=1 / fs)

    amplitude = 2 * np.abs(X) / N #dobler apmplituden for enkeltsidig spekter siden rfft() kun returnerer positive frekvenser, men to punkger skal ikke dobles

    # DCkomponenten skal ikke dobles (signalet sin middelverdi med 0hz og har ingen negativ speilfrekvens)
    amplitude[0] /= 2

    # Nyquist-komponenten skal heller ikke dobles da den ike har et egent speilpunkt
    if N % 2 == 0:
        amplitude[-1] /= 2

    return freq, amplitude


# Beregn enkeltsidig amplitudespekter
freq, amplitude = amplitude_spectrum(signal, fs)

plt.figure(figsize=(10, 4))
plt.stem(freq, amplitude, basefmt=" ")
plt.xlim(0, fs / 2)
plt.xlabel("Frekvens [Hz]")
plt.ylabel("Amplitude [V]")
plt.title("Enkeltsidig amplitudespekter")
plt.grid()
plt.tight_layout()
plt.show()


# Skriv ut frekvensoppløsningen
delta_f = freq[1] - freq[0]
print("Frekvensoppløsning:", delta_f, "Hz")


# Kontroller amplitudene ved de tre frekvensene
for forventet_frekvens in fk:
    indeks = np.argmin(np.abs(freq - forventet_frekvens))

    print(
        forventet_frekvens,
        "Hz:",
        amplitude[indeks],
        "V",
    )


# Sammenlign fft() og rfft()
signal_uten_dc = signal - np.mean(signal)
N = len(signal_uten_dc)

X_fft = np.fft.fft(signal_uten_dc)
freq_fft = np.fft.fftfreq(N, d=1 / fs)
amplitude_fft = np.abs(X_fft) / N

X_rfft = np.fft.rfft(signal_uten_dc)
freq_rfft = np.fft.rfftfreq(N, d=1 / fs)
amplitude_rfft = 2 * np.abs(X_rfft) / N

amplitude_rfft[0] /= 2

if N % 2 == 0:
    amplitude_rfft[-1] /= 2


fig, ax = plt.subplots(1, 2, figsize=(12, 4))

ax[0].stem(freq_fft, amplitude_fft, basefmt=" ")
ax[0].set_xlim(-1500, 1500)
ax[0].set_xlabel("Frekvens [Hz]")
ax[0].set_ylabel("Amplitude [V]")
ax[0].set_title("np.fft.fft()")
ax[0].grid()

ax[1].stem(freq_rfft, amplitude_rfft, basefmt=" ")
ax[1].set_xlim(0, 1500)
ax[1].set_xlabel("Frekvens [Hz]")
ax[1].set_ylabel("Amplitude [V]")
ax[1].set_title("np.fft.rfft()")
ax[1].grid()

plt.tight_layout()
plt.show()


# signalet er mer komplisert enn et enkelt isnussignal siden det er summen av tre sinskomopnenter som alle har ulike frekvenser og amplituder og faser
# de vil bygge på hverandre eller svekke hverandre avhengig av faseforskjellen mellom dem og tudspunktene som gir en ujven gr


# fft vil bergene hele frekvensspekter og retunerer både de positive og negastive frekvesene. Dette vil for e treeelt signal være at den negative delen er eet speibildea v den positive
# rfft() vil bare retunere frekvensen fra 0hz til nyquist frekvensen. Den er mer "effektiv" og passer godt til blant annet signalet som er brukt her
# fft er gjerne nyttig når signalet inneholder kompekse verdier eller om de positive og negative frekvensene har ulik betydning. For eksempel i moduleringsteknikker som AM og FM, hvor de positive og negative frekvensene representerer forskjellige deler av signalet (spennende lese opp på det).
