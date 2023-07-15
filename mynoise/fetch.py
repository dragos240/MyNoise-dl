import os
from typing import Optional

import requests

ASSET_DIR = "downloaded-assets/{}"


def parse_generator_name(url: str) -> str:
    parts = url.split("/")
    return parts[-2]


def parse_audio_file_name(url: str) -> str:
    parts = url.split("/")
    return parts[-1]


def fetch_from_url(url: str):
    """Download audio files for a given URL

    Args:
        url (str): URL to the generator
    """
    req = requests.get(url)
    content = req.text

    lines = [line.strip() for line in content.split("\n")]

    generator_name: Optional[str] = None
    data_path: Optional[str] = None
    found_urls_section: bool = False
    for line in lines:
        # Find the URLs for the audio files
        if "mynoise.world/Data" in line:
            found_urls_section = True
            # Extract the URL
            audio_url = line.split("'")[1] + ".ogg"
            if generator_name is None:
                # First pass sets the generator name and makes the data dir if
                # it doesn't exist
                generator_name = parse_generator_name(audio_url)
                data_path = ASSET_DIR.format(generator_name)
                os.makedirs(data_path, exist_ok=True)
            # Extract the filename
            audio_filename = parse_audio_file_name(audio_url)
            if "b.ogg" in audio_url:
                # There's both an 'a' and 'b' version for each slider, but we
                # don't need to have both
                continue
            # Fetch the audio content and write it to file
            audio = requests.get(audio_url).content
            audio_file_path = os.path.join(data_path, audio_filename)
            print(audio_file_path)
            with open(audio_file_path, 'wb') as f:
                f.write(audio)
        elif not found_urls_section:
            continue
        else:
            break


if __name__ == '__main__':
    print("Fetching from URL")
    fetch_from_url(
        "https://mynoise.net/NoiseMachines/loadingScreenSoundscapeGenerator.php")
    print("Done")
