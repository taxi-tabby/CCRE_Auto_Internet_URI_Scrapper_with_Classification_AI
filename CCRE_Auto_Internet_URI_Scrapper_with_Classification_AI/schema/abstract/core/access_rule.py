from abc import ABC, abstractmethod

class CCRE_AI_Scrapper_Access_Rule(ABC):



    @property
    @abstractmethod
    def skip_duplication_uri():
        """
        uri 중복을 건너뛸지 여부를 설정합니다
        """
        pass
    
    @skip_duplication_uri.setter
    @abstractmethod
    def skip_duplication_uri(self, value: bool):
        pass
    
    
    
    
    
    
    
    
    
    @property
    @abstractmethod
    def refresh_duplicate_uri():
        """
        uri 중복이 발생한 경우 해당 데이터를 갱신할지 여부를 설정합니다.
        건너뛰기 옵션이 비활성화 되어 있을 경우에만 작동합니다.
        횟수를 설정해야 합니다.
        """
        pass
    
    @refresh_duplicate_uri.setter
    @abstractmethod
    def refresh_duplicate_uri(self, value: bool):
        pass
    
    
    
    
    
    
    
    
    @property
    @abstractmethod
    def refresh_duplicate_uri_count():
        """
        uri 중복이 발생한 경우 해당 데이터를 갱신할지 여부에서 몇번 중복된 경우 갱신할지 설정합니다.
        """
        pass
    
    @refresh_duplicate_uri_count.setter
    @abstractmethod
    def refresh_duplicate_uri_count(self, value: int):
        pass