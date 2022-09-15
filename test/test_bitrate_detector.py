import os
import unittest

from detectors.bitrate_detector import BitrateDetector
from playlist.hls_parser import HLSParser


class TestBitrateDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(os.path.abspath(__file__))

    def test_detect_no_bitrate_change(self):
        data_file = os.path.join(self.cur_dir, "data/playlist_a_night_at_plaza.m3u8")
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        bitrate_detector = BitrateDetector()
        res = bitrate_detector.detect(m3_parser)
        assert res == True

    def test_detect_bitrate_change(self):
        data_file = os.path.join(
            self.cur_dir, "data/playlist_a_night_at_plaza_bitrate_changed.m3u8"
        )
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        bitrate_detector = BitrateDetector()
        res = bitrate_detector.detect(m3_parser)
        assert res == False
