#!/usr/bin/env python
import numpy as np
import numpy.fft as nf
from scipy.fft import fftfreq
import scipy.io.wavfile as wf
import matplotlib.pyplot as mp

LOWER_LIMIT = 20
UPPPERR_LIMIT = 20000

def denoise(wavfile):
    sample_rate, snd_data = wf.read(wavfile)
    snd_data = snd_data / (2 ** 14)
    times = np.arange(snd_data.size) / sample_rate

    mp.figure('Filter', facecolor='lightgray')
    mp.subplot(221)
    mp.title('Time Domain', fontsize=12)
    mp.xlabel('time, seconds', fontsize=12)
    mp.ylabel('snd_data', fontsize=12)
    mp.grid()
    mp.plot(times[:200], snd_data[:200], color='b', label='noised')
    mp.legend()
    mp.tight_layout()

    complex_ary = nf.fft(snd_data)

    # fft_freqs = nf.fftfreq(np.size(snd_data, 0), times[1]-times[0])
    fft_freqs = nf.fftfreq(np.size(snd_data, 0), 1/sample_rate)
    fft_pows = np.abs(complex_ary)
    print(fft_freqs[fft_freqs > 0].size)

    mp.subplot(222)
    mp.title('Frequency', fontsize=12)
    mp.xlabel('frequency, Hz', fontsize=12)
    mp.ylabel('pow', fontsize=12)
    mp.grid(linestyle=':')
    mp.semilogy(fft_freqs[fft_freqs > 0], fft_pows[fft_freqs > 0], color='orange', label='noised')
    mp.legend()
    mp.tight_layout()

    filtered_complex_ary = band_pass_filter(fft_freqs[fft_freqs > 0],
                                            complex_ary[fft_freqs > 0],
                                            LOWER_LIMIT,
                                            UPPPERR_LIMIT)
    filtered_fft_pows = np.abs(filtered_complex_ary)

    mp.subplot(224)
    mp.title('Filtered Frequency', fontsize=12)
    mp.xlabel('frequency, Hz', fontsize=12)
    mp.ylabel('pow', fontsize=12)
    mp.grid(linestyle=':')
    mp.semilogy(fft_freqs[fft_freqs > 0], filtered_fft_pows, color='orange', label='noised')
    mp.legend()
    mp.tight_layout()

    data = nf.ifft(filtered_fft_pows).real

    mp.subplot(223)
    mp.title('Filtered Time Domain', fontsize=12)
    mp.xlabel('time, seconds', fontsize=12)
    mp.ylabel('data', fontsize=12)
    mp.grid()
    mp.plot(times[:200], data[:200], color='b', label='filter')
    mp.legend()
    mp.tight_layout()

    wf.write('./records/filted.wav', sample_rate, (data * 2**14).astype(np.int16))

    mp.show()


def band_pass_filter(frequency, complex_ary, lower_limit, upper_limmit):
    """Read freqency data and filter out."""
    for idx, freq in enumerate(frequency):
        if freq < lower_limit:
            complex_ary[idx] = 0
        elif freq > upper_limmit:
            complex_ary[idx] = 0
    return complex_ary


if __name__ == '__main__':
    print('Start denoising...')
    denoise('./records/test.wav')
    print('Done')
