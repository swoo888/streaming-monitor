from detector_base import DetectorBase
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
        self.get_vtt_ts()
        if not self.check_caption():
            logging.warning(
                f"Found caption mismatch. uri: ${self._hls_parser.uri}, media segment {self._hls_parser.media_sequence}"
            )
            return True
        return False

    def get_vtt_ts(self):
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
            ts_list = self._ts_map.get(self._previous_media_sequence, [])
            vtt_list = self._vtt_map.get(self._previous_media_sequence, [])
            if set(ts_list) != set(vtt_list):
                return False
        del self._ts_map[self._previous_media_sequence]
        del self._vtt_map[self._previous_media_sequence]
        self._previous_media_sequence = cur_media_sequence
        return True
