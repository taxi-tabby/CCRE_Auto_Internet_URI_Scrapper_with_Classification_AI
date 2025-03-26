from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ValuableObject = TypeVar('ValuableObject')
MessageObjectGeneric = TypeVar('MessageObjectGeneric')

class CCRE_AI_Scrapper_QueueMessage(ABC, Generic[MessageObjectGeneric], Generic[ValuableObject]):



    @abstractmethod
    def set_message(self, type: MessageObjectGeneric, value: ValuableObject) -> "CCRE_AI_Scrapper_QueueMessage":
        """
        Set the message and return self for chaining
        """
        raise NotImplementedError