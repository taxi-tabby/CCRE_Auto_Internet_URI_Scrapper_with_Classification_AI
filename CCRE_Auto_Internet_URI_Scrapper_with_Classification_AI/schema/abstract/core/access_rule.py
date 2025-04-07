from abc import ABC, abstractmethod
from datetime import timedelta

class CCRE_AI_Scrapper_Access_Rule(ABC):



    @property
    @abstractmethod
    def robots_txt_expiration_time():
        """
        robots.txt 규칙의 만료 시간을 설정합니다 (timedelta 타입).
        """
        pass

    @robots_txt_expiration_time.setter
    @abstractmethod
    def robots_txt_expiration_time(self, value: timedelta):
        pass


    @property
    @abstractmethod
    def bot_name():
        """
        bot name을 설정합니다
        """
        pass
    
    @bot_name.setter
    @abstractmethod
    def bot_name(self, value: str):
        pass


    @property
    @abstractmethod
    def save_all_accessible_assets():
        """
        접근 가능한 모든 에셋(파일)을 저장 여부를 설정합니다.
        """
        pass

    @save_all_accessible_assets.setter
    @abstractmethod
    def save_all_accessible_assets(self, value: bool):
        pass

    @property
    @abstractmethod
    def save_all_accessible_assets_mime_types():
        """
        저장할 접근 가능한 에셋의 MIME 유형을 설정합니다.
        """
        pass

    @save_all_accessible_assets_mime_types.setter
    @abstractmethod
    def save_all_accessible_assets_mime_types(self, value: list[str]):
        pass
        

    @property
    @abstractmethod
    def scan_all_accessible_assets_for_malware():
        """
        접근 가능한 모든 에셋(파일)에 악성코드 검사를 할 것인지 설정합니다.
        """
        pass

    @scan_all_accessible_assets_for_malware.setter
    @abstractmethod
    def scan_all_accessible_assets_for_malware(self, value: bool):
        pass


    @property
    @abstractmethod
    def scan_all_accessible_assets_mime_types():
        """
        악성코드 검사를 수행할 MIME 유형을 설정합니다.
        """
        pass

    @scan_all_accessible_assets_mime_types.setter
    @abstractmethod
    def scan_all_accessible_assets_mime_types(self, value: list[str]):
        pass
        
















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