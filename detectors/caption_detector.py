from detectors.detector_base import DetectorBase
import logging
from playlist.hls_parser import HLSParser


class CaptionDetector(DetectorBase):
    def __init__(self) -> None:
        super().__init__()
        self._ts_map = {}
        self._vtt_map = {}
        self._hls_parser = None
        self._previous_media_sequence = None

    def detect(self, hls_parser) -> bool:
        self._hls_parser = hls_parser
        self.fill_vtt_ts()
        res = self.check_caption()
        if not res:
            logging.warning(
                f"Found caption mismatch. uri: ${self._hls_parser.uri}, media segment {self._hls_parser.media_sequence}"
            )
        return res

    def fill_vtt_ts(self):
        vtt_list = [
            segment.vtt_num
            for segment in self._hls_parser.segments
            if segment.vtt_num != HLSParser.NO_VTT_NUM
        ]
        ts_list = [
            segment.ts_num
            for segment in self._hls_parser.segments
            if segment.ts_num != HLSParser.NO_TS_NUM
        ]
        media_sequence = self._hls_parser.media_sequence
        self._vtt_map[media_sequence] = self._vtt_map.get(media_sequence, []) + vtt_list
        self._ts_map[media_sequence] = self._ts_map.get(media_sequence, []) + ts_list

    def check_caption(self) -> bool:
        cur_media_sequence = self._hls_parser.media_sequence
        if self._previous_media_sequence is None:
            self._previous_media_sequence = cur_media_sequence
        # media sequence advances to next number, check if previous sequence is matched
        if cur_media_sequence != self._previous_media_sequence:
            ts_list = self._ts_map.pop(self._previous_media_sequence, [])
            vtt_list = self._vtt_map.pop(self._previous_media_sequence, [])
            self._previous_media_sequence = cur_media_sequence
            if set(ts_list) != set(vtt_list):
                return False
        return True
