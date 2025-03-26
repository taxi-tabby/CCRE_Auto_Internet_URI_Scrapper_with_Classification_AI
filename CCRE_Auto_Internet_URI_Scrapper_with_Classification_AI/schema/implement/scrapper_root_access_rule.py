
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.core.access_rule import CCRE_AI_Scrapper_Access_Rule


class Scrapper_Root_Access_Rule(CCRE_AI_Scrapper_Access_Rule):
    def __init__(self, skip_duplication: bool = True):
        self._skip_uri_duplication = skip_duplication

    @property
    def skip_uri_duplication(self) -> bool:
        return self._skip_uri_duplication

    @skip_uri_duplication.setter
    def skip_uri_duplication(self, value: bool):
        self._skip_uri_duplication = value