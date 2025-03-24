from abc import ABC, abstractmethod

class CCRE_AI_Scrapper_Leaf(ABC):
    """
    Branch는 root에서 시작되어, root의 하위 개념입니다. 
    각각의 branch는 root에 다음 동작에 대한 큐를 입력하며
    """

    @abstractmethod
    def grow(self):
        """
        branch 에서 탐색을 시작합니다.
        """
        pass
        
