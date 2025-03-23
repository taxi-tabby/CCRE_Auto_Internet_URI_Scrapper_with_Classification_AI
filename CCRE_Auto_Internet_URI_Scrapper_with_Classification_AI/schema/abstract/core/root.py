from abc import ABC, abstractmethod

class CCRE_AI_Scrapper_Root(ABC):
    """
    root는 여러게일 가능성이 있으며, 각 뿌리에서 동시에 데이터를 수집합니다.
    root는 실행되는 쓰레드의 단위가 됩니다.
    """

    @abstractmethod
    def grow(self):
        """
        root 에서 탐색을 시작합니다.
        """
        pass
        
