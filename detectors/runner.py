import logging
from utils.timer import RepeatTimer
from playlist.hls_parser import HLSParser
from detectors.bitrate_detector import BitrateDetector
from detectors.caption_detector import CaptionDetector


class Runner:
    def __init__(self, uri, data_filepath=None) -> None:
        self._hls_parser = HLSParser(uri, data_filepath)
        self.set_up_detectors()

    def set_up_detectors(self) -> None:
        self._detectors = [
            BitrateDetector(),
            CaptionDetector(),
        ]
        # TODO(sw): maybe count some tags (DISCONTINUITY?), find episode boundaries..

    def run(self, repeat=True) -> None:
        try:
            self.detect()
            if repeat:
                timer = RepeatTimer(self._hls_parser.target_duration, self.detect)
                timer.start()
        except Exception as ex:
            logging.error(ex)

    def detect(self) -> bool:
        logging.debug(
            f"detecting uri:{self._hls_parser.uri}, data_filepath:{self._hls_parser.data_filepath}"
        )
        self._hls_parser.parse()
        for detector in self._detectors:
            detector.detect(self._hls_parser)
