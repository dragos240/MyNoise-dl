from math import ceil, floor
import os

from typing import List

from pydub import AudioSegment
from pydub.effects import normalize

ASSETS_PATH = "./downloaded-assets"


class GeneratedAudioFile:
    """Represents a generated audio file

    Attributes:
        samples: All loaded audio samples
    """
    samples: List[AudioSegment] = []

    @staticmethod
    def print_progress(step_name: str,
                       current_offset: int,
                       last_printed_percent: int,
                       total: int):
        current_percent = floor(current_offset / total * 100)
        if (current_percent - last_printed_percent) >= 10:
            print(f"{step_name}: {current_percent:d}%")

        return current_percent

    def load_file(self, path: str):
        """Load a audio file by path into `samples`

        Args:
            path (str): Path to the audio file
        """
        # Determine audio format and parse with corresponding parser
        if path.endswith(".ogg"):
            sample = self.parse_vorbis(path)
            self.samples.append(sample)

    def load_generator(self, name: str):
        """Load a generator by its name

        Args:
            name (str): Name of the generator

        Raises:
            Exception: If no generator exists by that name
        """
        fullpath = os.path.join(ASSETS_PATH, name)

        if os.path.exists(fullpath):
            for _, _, filenames in os.walk(fullpath):
                last_printed_percent: int = 0
                total = len(filenames)
                for filename_idx, filename in enumerate(filenames):
                    last_printed_percent \
                        = self.print_progress("Loading files",
                                              filename_idx,
                                              last_printed_percent,
                                              total)
                    self.load_file(os.path.join(fullpath, filename))
        else:
            raise Exception("ERR: No generator by that name: ")

    def find_generators(self) -> List[str]:
        """Find downloaded generators

        Returns:
            List[str]: A `List` of all downloaded generators
        """
        generators = []
        for _, dirnames, _ in os.walk(ASSETS_PATH):
            for dirname in dirnames:
                # Make sure there are files inside these directories
                fullpath = os.path.join(ASSETS_PATH, dirname)
                for _, _, filenames in os.walk(fullpath):
                    if len(filenames) == 0:
                        break
                    generators.append(dirname)
                    break

        return generators

    def parse_vorbis(self, file_path: str) -> AudioSegment:
        """Load an ogg Vorbis file into an `AudioSegment`

        Args:
            file_path (str): Path to load

        Returns:
            AudioSegment: The AudioSegment to return
        """
        sample: AudioSegment = AudioSegment.from_ogg(file_path)

        return sample

    def recursively_overlay(self, length: str) -> AudioSegment:
        """Overlay all loaded samples over each other into an `AudioSegment`

        Args:
            length (str): Length of `AudioSegment` in format [min:]sec

        Returns:
            AudioSegment: The resulting `AudioSegment`

        Raises:
            SyntaxError: Wrong format for `length`
        """
        secs = 0
        if ':' in length:
            if length.count(":") == 1:
                parts = length.split(":")
                secs = int(parts[0]) * 60
                secs += int(parts[1])
            else:
                raise SyntaxError(
                    "Must be mins:sec or sec. Any other format is unsupported")
        else:
            secs = int(length)
        looped_samples: List[AudioSegment] = []
        time_in_ms: int = secs * 1000
        len_samples: int = len(self.samples)
        last_printed_percent: int = 0
        idx: int
        for sample_idx, sample in enumerate(self.samples):
            last_printed_percent = self.print_progress("Overlaying",
                                                       sample_idx,
                                                       last_printed_percent,
                                                       len_samples)
            combined = AudioSegment.empty()
            n_loops = ceil(time_in_ms / len(sample))
            # Make enough loops to fill up time_in_ms
            for _ in range(n_loops):
                combined = combined + sample
            looped_samples.append(combined)
        overlayed = AudioSegment.silent(time_in_ms)
        for looped_sample in looped_samples:
            looped_sample = normalize(looped_sample, headroom=4)
            # Overlay the samples
            overlayed = overlayed.overlay(looped_sample)
            # Normalize the volume
            overlayed = normalize(overlayed, headroom=4)

        return overlayed[:time_in_ms]


if __name__ == '__main__':
    af = GeneratedAudioFile()
    assets_dir = "downloaded-assets/nowloading"
    af.load_generator("nowloading")
    result: AudioSegment = af.recursively_overlay("1:30")
    if isinstance(result, AudioSegment):
        result.export("out.wav", format='wav')
