from argparse import ArgumentParser
import logging
from detectors.runner import Runner


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Running....")
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-i", "--uri", default="", help="uri link to m3u8 playlist")
    arg_parser.add_argument(
        "-f", "--file", default="", help="file path to m3u8 playlis file"
    )
    args = arg_parser.parse_args()
    Runner(args.uri, args.file).run()


if __name__ == "__main__":
    main()
