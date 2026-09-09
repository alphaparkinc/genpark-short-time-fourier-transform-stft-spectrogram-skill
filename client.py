"""
Autonomous Agent Short-Time Fourier Transform (STFT) Skill
Pure Python Standard Library implementation.
"""
import math
import cmath
from typing import List, Dict, Any

class STFTAnalyzer:
    """
    STFT Time-Frequency Spectrogram Generator with Hann windowing.
    """
    @staticmethod
    def _fft(x: List[complex]) -> List[complex]:
        n = len(x)
        if n <= 1:
            return list(x)
        even = STFTAnalyzer._fft(x[0::2])
        odd = STFTAnalyzer._fft(x[1::2])
        t = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
        return [even[k] + t[k] for k in range(n // 2)] + [even[k] - t[k] for k in range(n // 2)]

    @staticmethod
    def compute_spectrogram(signal: List[float], window_size: int = 4, hop_size: int = 2) -> List[List[float]]:
        # Power of 2 check
        p2 = 1
        while p2 < window_size:
            p2 <<= 1
        w_size = p2

        window = [0.5 * (1 - math.cos(2 * math.pi * n / max(1, w_size - 1))) for n in range(w_size)]
        spectrogram = []

        for i in range(0, len(signal) - w_size + 1, hop_size):
            segment = [signal[i + k] * window[k] for k in range(w_size)]
            complex_seg = [complex(v, 0.0) for v in segment]
            fft_res = STFTAnalyzer._fft(complex_seg)
            magnitudes = [round(abs(val), 4) for val in fft_res[:w_size // 2 + 1]]
            spectrogram.append(magnitudes)

        return spectrogram
