from ..abstract.core.root import CCRE_AI_Scrapper_Root

class Scrapper_Root(CCRE_AI_Scrapper_Root):
    def __init__(self, root_key: str, root_uri: str):
        self._root_key = root_key
        self._root_uri = root_uri

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
        
        
    def init(self):
        pass
