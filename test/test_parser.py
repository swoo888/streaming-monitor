import m3u8
import os
from playlist.hls_parser import HLSParser
import unittest


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(
            self.cur_dir, "data/playlist_a_night_at_plaza.m3u8"
        )

    @unittest.skip
    def test_data(self):
        text_file = open(self.data_file)
        data = text_file.read()
        text_file.close()
        m3u8_obj = m3u8.loads(data)
        print(m3u8_obj.dumps())

    def test_load(self):
        m3_parser = HLSParser(None, self.data_file)
        ok = m3_parser.load_m3u8()
        assert ok is True
        assert m3_parser.m3u8_item is not None

    def test_parse(self):
        m3_parser = HLSParser(None, self.data_file)
        ok = m3_parser.parse()
        assert ok == True
        assert m3_parser.is_variant == False
        assert m3_parser.target_duration == 5
        assert m3_parser.media_sequence == 113
        assert m3_parser.discontinuity_sequence == 11
        assert len(m3_parser.segments) == 5
        for segment in m3_parser.segments:
            assert segment.duration == 5
            assert segment.resolution == 720
