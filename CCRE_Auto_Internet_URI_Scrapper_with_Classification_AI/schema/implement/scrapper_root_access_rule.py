import json
from datetime import timedelta
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.core.access_rule import CCRE_AI_Scrapper_Access_Rule


class Scrapper_Root_Access_Rule(CCRE_AI_Scrapper_Access_Rule):
    def __init__(self, 
                 skip_duplication_uri: bool = True,
                 refresh_duplicate_uri: bool = False,
                 refresh_duplicate_uri_count: int = 0,
                 queue_upload_delay_seconds: int = 1,
                 consume_delay_seconds: int = 1,
                 robots_txt_expiration_time: timedelta = timedelta(days=1),
                 save_all_accessible_assets: bool = False,
                 save_all_accessible_assets_mime_types: list[str] = None,
                 scan_all_accessible_assets_for_malware: bool = False,
                 scan_all_accessible_assets_mime_types: list[str] = None):
        
        """
        Initializes the ScrapperRootAccessRule class with various configuration options.
        Args:
            skip_duplication_uri (bool): Determines whether to skip duplicate URIs. Defaults to True.
            refresh_duplicate_uri (bool): Indicates whether to refresh duplicate URIs. Defaults to False.
            refresh_duplicate_uri_count (int): The number of times to refresh duplicate URIs. Defaults to 0.
            queue_upload_delay_seconds (int): Delay in seconds for queue uploads. Defaults to 1.
            consume_delay_seconds (int): Delay in seconds between consuming URIs. Defaults to 1.
            robots_txt_expiration_time (timedelta): Expiration time for robots.txt rules. Defaults to 1 day.
            save_all_accessible_assets (bool): Whether to save all accessible assets. Defaults to False.
            save_all_accessible_assets_mime_types (list[str]): List of MIME types to save for accessible assets. Defaults to None.
            scan_all_accessible_assets_for_malware (bool): Whether to scan all accessible assets for malware. Defaults to False.
            scan_all_accessible_assets_mime_types (list[str]): List of MIME types to scan for malware. Defaults to None.
        """
        
        
        self._skip_duplication_uri = skip_duplication_uri
        self._refresh_duplicate_uri = refresh_duplicate_uri
        self._refresh_duplicate_uri_count = refresh_duplicate_uri_count
        self._queue_upload_delay_seconds = queue_upload_delay_seconds
        self._consume_delay_seconds = consume_delay_seconds
        self._robots_txt_expiration_time = robots_txt_expiration_time
        self._save_all_accessible_assets = save_all_accessible_assets
        self._save_all_accessible_assets_mime_types = save_all_accessible_assets_mime_types or []
        self._scan_all_accessible_assets_for_malware = scan_all_accessible_assets_for_malware
        self._scan_all_accessible_assets_mime_types = scan_all_accessible_assets_mime_types or []





    # skip_duplication_uri
    @property
    def skip_duplication_uri(self) -> bool:
        return self._skip_duplication_uri

    @skip_duplication_uri.setter
    def skip_duplication_uri(self, value: bool):
        self._skip_duplication_uri = value

    # refresh_duplicate_uri
    @property
    def refresh_duplicate_uri(self) -> bool:
        return self._refresh_duplicate_uri

    @refresh_duplicate_uri.setter
    def refresh_duplicate_uri(self, value: bool):
        self._refresh_duplicate_uri = value

    # refresh_duplicate_uri_count
    @property
    def refresh_duplicate_uri_count(self) -> int:
        return self._refresh_duplicate_uri_count

    @refresh_duplicate_uri_count.setter
    def refresh_duplicate_uri_count(self, value: int):
        self._refresh_duplicate_uri_count = value


    # queue_upload_delay_seconds
    @property
    def queue_upload_delay_seconds(self) -> int:
        """
        Sets the delay time for queue uploads in seconds.
        """
        return self._queue_upload_delay_seconds

    @queue_upload_delay_seconds.setter
    def queue_upload_delay_seconds(self, value: int):
        self._queue_upload_delay_seconds = value


    # consume_delay_seconds
    @property
    def consume_delay_seconds(self) -> int:
        return self._consume_delay_seconds

    @consume_delay_seconds.setter
    def consume_delay_seconds(self, value: int):
        self._consume_delay_seconds = value





    # robots_txt_expiration_time
    @property
    def robots_txt_expiration_time(self) -> timedelta:
        return self._robots_txt_expiration_time

    @robots_txt_expiration_time.setter
    def robots_txt_expiration_time(self, value: timedelta):
        self._robots_txt_expiration_time = value

    # save_all_accessible_assets
    @property
    def save_all_accessible_assets(self) -> bool:
        return self._save_all_accessible_assets

    @save_all_accessible_assets.setter
    def save_all_accessible_assets(self, value: bool):
        self._save_all_accessible_assets = value

    # save_all_accessible_assets_mime_types
    @property
    def save_all_accessible_assets_mime_types(self) -> list[str]:
        return self._save_all_accessible_assets_mime_types

    @save_all_accessible_assets_mime_types.setter
    def save_all_accessible_assets_mime_types(self, value: list[str]):
        self._save_all_accessible_assets_mime_types = value

    # scan_all_accessible_assets_for_malware
    @property
    def scan_all_accessible_assets_for_malware(self) -> bool:
        return self._scan_all_accessible_assets_for_malware

    @scan_all_accessible_assets_for_malware.setter
    def scan_all_accessible_assets_for_malware(self, value: bool):
        self._scan_all_accessible_assets_for_malware = value

    # scan_all_accessible_assets_mime_types
    @property
    def scan_all_accessible_assets_mime_types(self) -> list[str]:
        return self._scan_all_accessible_assets_mime_types

    @scan_all_accessible_assets_mime_types.setter
    def scan_all_accessible_assets_mime_types(self, value: list[str]):
        self._scan_all_accessible_assets_mime_types = value

    # JSON serialization
    def to_json(self) -> str:
        """Convert the internal variables to a JSON string."""
        return json.dumps({
            "skip_duplication_uri": self._skip_duplication_uri,
            "refresh_duplicate_uri": self._refresh_duplicate_uri,
            "refresh_duplicate_uri_count": self._refresh_duplicate_uri_count,
            "consume_delay_seconds": self._consume_delay_seconds,
            "robots_txt_expiration_time": self._robots_txt_expiration_time.total_seconds(),
            "save_all_accessible_assets": self._save_all_accessible_assets,
            "save_all_accessible_assets_mime_types": self._save_all_accessible_assets_mime_types,
            "scan_all_accessible_assets_for_malware": self._scan_all_accessible_assets_for_malware,
            "scan_all_accessible_assets_mime_types": self._scan_all_accessible_assets_mime_types
        })
        
    def put_json(self, data: dict | None) -> None:
        """
        Updates the object's attributes using the provided dictionary.
        
        Args:
            data (dict): Dictionary containing the data to update the object.
        
        Raises:
            ValueError: If the provided data is None or not a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary and cannot be None.")

        self._skip_duplication_uri = data.get("skip_duplication_uri", self._skip_duplication_uri)
        self._refresh_duplicate_uri = data.get("refresh_duplicate_uri", self._refresh_duplicate_uri)
        self._refresh_duplicate_uri_count = data.get("refresh_duplicate_uri_count", self._refresh_duplicate_uri_count)
        self._consume_delay_seconds = data.get("consume_delay_seconds", self._consume_delay_seconds)
        self._robots_txt_expiration_time = timedelta(seconds=data.get("robots_txt_expiration_time", self._robots_txt_expiration_time.total_seconds()))
        self._save_all_accessible_assets = data.get("save_all_accessible_assets", self._save_all_accessible_assets)
        self._save_all_accessible_assets_mime_types = data.get("save_all_accessible_assets_mime_types", self._save_all_accessible_assets_mime_types)
        self._scan_all_accessible_assets_for_malware = data.get("scan_all_accessible_assets_for_malware", self._scan_all_accessible_assets_for_malware)
        self._scan_all_accessible_assets_mime_types = data.get("scan_all_accessible_assets_mime_types", self._scan_all_accessible_assets_mime_types)


    def __repr__(self):
        return super().__repr__()