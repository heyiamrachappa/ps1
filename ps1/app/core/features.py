from abc import ABC, abstractmethod
import numpy as np
import librosa
from scipy.ndimage import maximum_filter
from scipy.ndimage import binary_erosion

class FeatureExtractor(ABC):
    """Issue 3: Develop Audio Feature Extraction Interface"""
    @abstractmethod
    def extract(self, audio_path: str) -> np.ndarray:
        pass

class BaselineFingerprinter(FeatureExtractor):
    """Issue 4: Implement Baseline Fingerprinting Logic (Constellation Mapping)"""
    def __init__(self, sample_rate=22050, n_fft=2048, hop_length=512):
        self.sr = sample_rate
        self.n_fft = n_fft
        self.hop_length = hop_length

    def extract(self, audio_path: str) -> np.ndarray:
        # Load audio and normalize volume
        y, _ = librosa.load(audio_path, sr=self.sr)
        y = librosa.util.normalize(y)
        
        # Compute Spectrogram
        S = np.abs(librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length))
        
        # Issue 8 & 15: Mel-Frequency Banding (More robust than raw bins)
        S_mel = librosa.feature.melspectrogram(S=S**2, sr=self.sr, n_mels=128)
        S_db = librosa.power_to_db(S_mel, ref=np.max)
        
        # Find local peaks in the Mel-spectrogram
        peaks = self._get_2d_peaks(S_db)
        return peaks

    def _get_2d_peaks(self, S_db, threshold=-40, neighborhood_size=10):
        """Find local peaks in the Mel-spectrogram (Optimized for robustness)."""
        data_max = maximum_filter(S_db, neighborhood_size)
        maxima = (S_db == data_max)
        maxima &= (S_db > threshold)
        
        peaks = np.argwhere(maxima)
        return peaks

def generate_hashes(peaks, fan_value=15):
    """
    Generate hashes from peaks. 
    A hash is (freq1, freq2, delta_time) paired with an offset (time1).
    """
    hashes = []
    # Sort peaks by time
    peaks = peaks[peaks[:, 1].argsort()]
    
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):
                f1, t1 = peaks[i]
                f2, t2 = peaks[i + j]
                dt = t2 - t1
                
                # Increased dt range to 300 for better robustness
                if 0 < dt < 300: 
                    # Create a unique hash
                    h = (int(f1), int(f2), int(dt))
                    hashes.append((h, int(t1)))
    return hashes
