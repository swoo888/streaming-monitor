import os
import unittest

from detectors.caption_detector import CaptionDetector
from playlist.hls_parser import HLSParser


class TestCaptionDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(
            self.cur_dir, "data/playlist_a_night_at_plaza.m3u8"
        )

    def test_detect_matched(self):
        data_file = os.path.join(self.cur_dir, "data/playlist_caption_seq186_ts.m3u8")
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        caption_detector = CaptionDetector()
        res = caption_detector.detect(m3_parser)
        # No captions missing since it only has ts list
        assert res == True

        # load vtt list
        data_file = os.path.join(self.cur_dir, "data/playlist_caption_seq186_vtt.m3u8")
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        res = caption_detector.detect(m3_parser)
        assert res == True

        # load next sequence ts list
        data_file = os.path.join(self.cur_dir, "data/playlist_caption_seq187_ts.m3u8")
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        res = caption_detector.detect(m3_parser)
        # assert ts and vtt match
        assert res == True

    def test_detect_unmatched(self):
        data_file = os.path.join(self.cur_dir, "data/playlist_caption_seq186_ts.m3u8")
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        caption_detector = CaptionDetector()
        res = caption_detector.detect(m3_parser)
        # No captions missing since it only has ts list
        assert res == True

        # load vtt list
        data_file = os.path.join(
            self.cur_dir, "data/playlist_caption_seq186_vtt_unmatched.m3u8"
        )
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        res = caption_detector.detect(m3_parser)
        assert res == True

        # load next sequence ts list
        data_file = os.path.join(self.cur_dir, "data/playlist_caption_seq187_ts.m3u8")
        m3_parser = HLSParser(None, data_file)
        m3_parser.parse()
        res = caption_detector.detect(m3_parser)
        # assert ts and vtt match
        assert res == False
