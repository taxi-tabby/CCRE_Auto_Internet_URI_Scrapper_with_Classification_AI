from abc import ABC, abstractmethod

class CCRE_AI_Scrapper_Access_Rule(ABC):

    def __init__(self, 
                 skip_uri_duplication: bool = True
                 ):
        self._skip_uri_duplication = skip_uri_duplication

    @property
    @abstractmethod
    def skip_uri_duplication():
        """
        uri 중복을 건너뛸지 여부를 반환합니다
        """
        pass
    
    @skip_uri_duplication.setter
    @abstractmethod
    def skip_uri_duplication(self, value: bool):
        pass