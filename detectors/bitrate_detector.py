from detector_base import DetectorBase
import logging
from playlist.hls_parser import HLSParser


class BitrateDetector(DetectorBase):
    def __init__(self) -> None:
        super().__init__()
        self._last_resolution = None

    def detect(self, hls_parser) -> bool:
        for segment in hls_parser.segments:
            resolution = segment.resolution
            if self._last_resolution is None:
                self._last_resolution = resolution
            elif resolution != self._last_resolution:
                logging.warning(
                    f"!!!!resolution shift, uri: {segment.absolute_uri}, "
                    f"resolution: {resolution}"
                )
                return True
        return False
