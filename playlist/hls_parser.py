import logging
import m3u8
import re


class HLSParser:
    # ex. https://somesite.net/944_pluto/clip/
    #       6206b938a0a48f0013d5cb1b_A_Night_at_the_Plaza/
    #       720p/20220211_113000/hls/1067069-end/hls_2400-00012.ts
    # 720p is the resolution
    RESOLUTION_MATCH = r"/(\d+)p/"
    # 12 is the media number in hls_2400-00012.ts
    TS_MATCH = r"/*-0*(\d+)\.ts"

    # https://siloh-fs.plutotv.net/952_pluto/clip/
    #       620e76a0a0a48f0013d9a471_Scary_Movie_3/720p/20220217_082400/
    #       hls/3960170-end/en/en.m3u8_0000000186.vtt
    # 186 is media number in en.m3u8_0000000186.vtt
    VTT_MATCH = r"/*_0*(\d+)\.vtt"

    NO_VTT_NUM = -1
    NO_TS_NUM = -1

    def __init__(self, uri, data_filepath=None) -> None:
        self._m3u8_item = None
        self._resolution_match = re.compile(HLSParser.RESOLUTION_MATCH)
        self._ts_match = re.compile(HLSParser.TS_MATCH)
        self._vtt_match = re.compile(HLSParser.VTT_MATCH)
        self.uri = uri
        self.data_filepath = data_filepath

    def load_m3u8(self) -> bool:
        if (not self.uri and not self.data_filepath) or (
            self.uri and self.data_filepath
        ):
            logging.error("Must provide the media uri or file path.")
            return False
        try:
            if self.uri is not None:
                self._m3u8_item = m3u8.load(self.uri)
            elif self.data_filepath is not None:
                with open(self.data_filepath) as data:
                    playlist = data.read()
                    self._m3u8_item = m3u8.loads(playlist)
            return True
        except Exception as ex:
            logging.error(
                (
                    f"Unable to read m3u8, uri: {self.uri}, "
                    f"data_filepath: {self.data_filepath}"
                    f"ex: {ex}"
                )
            )
            return False

    def parse(self) -> bool:
        logging.info(f"parsing uri:{self.uri}, data_filepath:{self.data_filepath}")
        if not self.load_m3u8():
            return False
        self.process_segments()
        return True

    def process_segments(self) -> None:
        segments = self._m3u8_item.segments
        for segment in segments:
            segment.resolution = self.get_resolution(segment.absolute_uri)
            segment.vtt_number = self.get_vtt_num(segment.absolute_uri)
            segment.ts_number = self.get_ts_num(segment.absolute_uri)
            logging.info(f"resolution is: {segment.resolution}")

    def get_vtt_num(self, seg_uri) -> int:
        res = self._vtt_match.search(seg_uri)
        if res is None:
            return HLSParser.NO_VTT_NUM
        return int(res.group(1))

    def get_ts_num(self, seg_uri) -> int:
        res = self._ts_match.search(seg_uri)
        if res is None:
            return HLSParser.NO_TS_NUM
        return int(res.group(1))

    def get_resolution(self, seg_uri) -> int:
        res = self._resolution_match.search(seg_uri)
        if res is None:
            raise Exception("No resolution in uri: {}".format(seg_uri))
        return int(res.group(1))

    @property
    def target_duration(self, default=5) -> int:
        return getattr(self._m3u8_item, "target_duration", default)

    @property
    def media_sequence(self, default=0) -> int:
        return getattr(self._m3u8_item, "media_sequence", default)

    @property
    def discontinuity_sequence(self, default=0) -> int:
        return getattr(self._m3u8_item, "discontinuity_sequence", default)

    @property
    def is_variant(self) -> bool:
        return self._m3u8_item.is_variant

    @property
    def segments(self) -> list:
        return self._m3u8_item.segments

    @property
    def m3u8_item(self) -> object:
        return self._m3u8_item
