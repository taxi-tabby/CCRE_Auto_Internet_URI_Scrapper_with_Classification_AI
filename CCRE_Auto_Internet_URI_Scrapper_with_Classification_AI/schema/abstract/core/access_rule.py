from abc import ABC, abstractmethod
from datetime import timedelta

class CCRE_AI_Scrapper_Access_Rule(ABC):


    @property
    @abstractmethod
    def queue_upload_delay_seconds():
        """
        URI 당 queue에 업로드되는 딜레이를 정의합니다.
        이 값은 소비 지연 시간과 마찬가지로 성능에 영향응 크기 끼칩니다.
        하나의 uri 에서 발견화는 다른 uri 가 100초이고 지연이 1초로 정의되어 있다면 업로드 완료까지 100+a 초가 소요됩니다.
        폭발적으로 입력되는 경우 성능의 저하가 발생할 수 있으니 해당 값을 조정하여 성능을 조율 가능합니다.
        """
        pass

    @queue_upload_delay_seconds.setter
    @abstractmethod
    def queue_upload_delay_seconds(self, value: int):
        pass



    @property
    @abstractmethod
    def consume_delay_seconds():
        """
        소비 지연 시간을 초 단위로 설정합니다.
        이 값은 성능에 큰 영향을 미칩니다.
        소비 지연 시간은 큐에서 메시지를 소비하는 데 걸리는 시간을 나타냅니다.
        이 값이 너무 작으면 소비 속도가 빨라져서 시스템에 부하를 줄 수 있습니다.
        반대로 너무 크면 소비 속도가 느려져서 탐색 속도의 저하를 초래할 수 있습니다
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