from math import ceil
import os

from typing import List, Tuple
from pydub import AudioSegment
from pydub.effects import normalize

ASSETS_PATH = "./downloaded-assets"


class AudioFile:
    """Audio data and loading"""
    samples: List[AudioSegment]

    def __init__(self) -> None:
        self.samples = []

    def load_file(self, filename: str):
        # Determine audio format and parse with corresponding parser
        if filename.endswith(".ogg"):
            sample = self.parse_vorbis(filename)
            self.samples.append(sample)

    def parse_vorbis(self, filename) -> AudioSegment:
        sample: AudioSegment = AudioSegment.from_ogg(filename)

        return sample

    def recursively_overlay(self, secs: int) -> AudioSegment:
        looped_samples: List[AudioSegment] = []
        time_in_ms = secs * 1000
        for sample in self.samples:
            combined = AudioSegment.empty()
            n_loops = ceil(time_in_ms / len(sample))
            # Make enough loops to fill up time_in_ms
            for _ in range(n_loops):
                combined = combined + sample
            looped_samples.append(combined)
        overlayed = AudioSegment.silent(time_in_ms)
        for looped_sample in looped_samples:
            # Overlay the samples
            overlayed = overlayed.overlay(looped_sample)
            # Normalize the volume
            overlayed = normalize(overlayed, headroom=2)

        if isinstance(overlayed, AudioSegment):
            return overlayed[:time_in_ms]
        else:
            raise Exception("A")


if __name__ == '__main__':
    af = AudioFile()
    assets_dir = "downloaded-assets/nowloading"
    for _, _, filenames in os.walk(assets_dir):
        for filename in filenames:
            af.load_file(os.path.join(assets_dir, filename))
    result: AudioSegment = af.recursively_overlay(120)
    if isinstance(result, AudioSegment):
        result.export("out.wav", format='wav')
