#!/usr/bin/env python3
import argparse

from pydub import AudioSegment

from mynoise.audio import GeneratedAudioFile
from mynoise.fetch import fetch_from_url


def main(args: argparse.Namespace, parser: argparse.ArgumentParser):
    af = GeneratedAudioFile()

    if args.list:
        gens = af.find_generators()
        print("\n".join(gens))
        return
    if args.generator:
        generator: str = args.generator
        if generator.startswith("https"):
            generator = fetch_from_url(generator)
        af.load_generator(generator)
        result: AudioSegment = af.recursively_overlay(args.length)
        filename: str = args.output_file
        extension = filename.split(".")[-1]

        print("Exporting...")
        result.export(filename, format=extension)
        print("Exported generator to", filename)
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generator",
                        help="Generator name or URL to a generator page",
                        type=str,
                        metavar="GENERATOR")
    parser.add_argument("-l", "--list",
                        help="List collected generators",
                        action="store_true")
    parser.add_argument("-t", "--length",
                        help="How long the file should be (in seconds)",
                        type=str,
                        metavar="LENGTH",
                        default="60")
    parser.add_argument("-o", "--output-file",
                        help="Path to the output file (including extnension)",
                        default="out.wav",
                        type=str)

    args = parser.parse_args()
    main(args, parser)
