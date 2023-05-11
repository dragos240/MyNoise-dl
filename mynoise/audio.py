import wave

from pyogg import VorbisFile
import pyaudio

ASSETS_PATH = "./downloaded-assets"


class AudioFile:
    """Audio data and loading"""

    def load_file(self, filename: str):
        self.sample_width = 0
        self.channels = 0
        self.sample_rate = 0
        self.n_frames = 0
        self.frames = []
        # Determine audio format and parse with corresponding parser
        if filename.endswith(".ogg"):
            self.parse_vorbis(filename)

        # Store result
        pass

    def parse_vorbis(self, filename):
        vf = VorbisFile(filename)
        self.sample_width = 1
        self.channels = vf.channels
        self.sample_rate = vf.frequency
        self.n_frames = vf.buffer_length
        self.frames = vf.buffer
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(self.sample_width),
                        channels=self.channels,
                        rate=self.sample_rate,
                        output=True)

        stream.write(self.frames)

        stream.stop_stream()
        stream.close()

        p.terminate()


if __name__ == '__main__':
    af = AudioFile()
    af.parse_vorbis("tests/res/sounds/0a.ogg")
