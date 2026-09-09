"""Example usage for STFT Spectrogram Skill."""
from client import STFTAnalyzer
import math

def main():
    print("Executing Short-Time Fourier Transform...")
    data = [math.sin(0.2 * i) for i in range(16)]
    spectrogram = STFTAnalyzer.compute_spectrogram(data, window_size=4, hop_size=2)
    print(f"Generated {len(spectrogram)} temporal frames:")
    for frame in spectrogram:
        print(" ", frame)
    assert len(spectrogram) > 0
    print("STFT Spectrogram verified successfully!")

if __name__ == "__main__":
    main()
