from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.core.access_rule import CCRE_AI_Scrapper_Access_Rule
from ..abstract.core.root import CCRE_AI_Scrapper_Root

class Scrapper_Root(CCRE_AI_Scrapper_Root):
    def __init__(self, root_key: str, root_uri: str, access_rule: CCRE_AI_Scrapper_Access_Rule):
        self._root_key = root_key
        self._root_uri = root_uri
        self._access_rule = access_rule

    @property
    def root_key(self):
        return self._root_key

    @root_key.setter
    def root_key(self, value: str):
        self._root_key = value

    @property
    def root_uri(self):
        return self._root_uri

    @root_uri.setter
    def root_uri(self, value: str):
        self._root_uri = value
        
        
    @property
    def access_rule(self):
        return self._access_rule
    
    @access_rule.setter
    def access_rule(self, value: CCRE_AI_Scrapper_Access_Rule):
        self._access_rule = value
        
        
    def init(self):
        pass
