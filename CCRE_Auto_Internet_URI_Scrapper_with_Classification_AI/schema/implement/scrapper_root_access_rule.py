
import json
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.core.access_rule import CCRE_AI_Scrapper_Access_Rule


class Scrapper_Root_Access_Rule(CCRE_AI_Scrapper_Access_Rule):
    def __init__(self, 
                    skip_duplication_uri: bool = True,
                    refresh_duplicate_uri: bool = False,
                    refresh_duplicate_uri_count: int = 0
                 ):
        
        self._skip_duplication_uri = skip_duplication_uri
        self._refresh_duplicate_uri = refresh_duplicate_uri
        self._refresh_duplicate_uri_count = refresh_duplicate_uri_count

    @property
    def skip_duplication_uri(self) -> bool:
        return self._skip_duplication_uri

    @skip_duplication_uri.setter
    def skip_duplication_uri(self, value: bool):
        self._skip_duplication_uri = value
        

    @property
    def refresh_duplicate_uri(self) -> bool:
        return self._refresh_duplicate_uri
    
    @refresh_duplicate_uri.setter
    def refresh_duplicate_uri(self, value: bool):
        self._refresh_duplicate_uri = value
    
    

    @property
    def refresh_duplicate_uri_count(self) -> int:
        return self._refresh_duplicate_uri_count        
    
    @refresh_duplicate_uri_count.setter
    def refresh_duplicate_uri_count(self, value: int):
        self._refresh_duplicate_uri_count = value
        
    def to_json(self) -> str:
        """Convert the internal variables to a JSON string."""
        return json.dumps({
            "skip_duplication_uri": self._skip_duplication_uri,
            "refresh_duplicate_uri": self._refresh_duplicate_uri,
            "refresh_duplicate_uri_count": self._refresh_duplicate_uri_count
        })