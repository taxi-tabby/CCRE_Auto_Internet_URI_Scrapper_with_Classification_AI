from abc import ABC, abstractmethod
from datetime import timedelta

class CCRE_AI_Scrapper_Access_Rule(ABC):




    @property
    @abstractmethod
    def consume_delay_seconds():
        """
        소비 지연 시간을 초 단위로 설정합니다.
        """
        pass

    @consume_delay_seconds.setter
    @abstractmethod
    def consume_delay_seconds(self, value: int):
        pass



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
    
    
    @abstractmethod
    def to_json(self) -> str:
        """
        객체의 속성을 JSON 문자열로 변환합니다.
        """
        pass
    
    @abstractmethod
    def put_json(self, data: dict | None) -> None:
        """
        객체 json 데이터를 해당 오브젝트에 입력합니다.
        :param data: 객체에 입력할 JSON 데이터의 딕셔너리 형태
        """
        pass
    
    
    
    def __repr__(self) -> str:
        """
        객체의 속성을 문자열로 표현합니다.
        """
        attributes = ", ".join(
            f"{attr}={getattr(self, attr, None)!r}" 
            for attr in dir(self) 
            if not attr.startswith("_") and not callable(getattr(self, attr, None))
        )
        return f"<{self.__class__.__name__}({attributes})>"