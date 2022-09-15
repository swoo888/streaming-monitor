from abc import ABC, abstractmethod
from playlist.hls_parser import HLSParser


class DetectorBase(ABC):
    @abstractmethod
    def detect(self, hls_parser: HLSParser):
        pass
