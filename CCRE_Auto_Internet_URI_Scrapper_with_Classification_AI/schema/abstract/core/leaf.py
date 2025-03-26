from abc import ABC, abstractmethod

class CCRE_AI_Scrapper_Leaf(ABC):
    """
    leaf 는 식별하는 객체입니다
    """

    @abstractmethod
    def ob_text(self, binary: bytes):
        """
        text를 식별합니다
        """
        pass
    
    @abstractmethod
    def ob_image_png(self, binary: bytes):
        """
        png 식별합니다
        """
        pass
        
    @abstractmethod
    def ob_image_jpeg(self, binary: bytes):
        """
        jpeg 식별합니다
        """
        pass
    
    @abstractmethod
    def ob_image_svg(self, binary: bytes):
        """
        svg 식별합니다
        """
        pass

    @abstractmethod
    def ob_image_mp3(self, binary: bytes):
        """
        mp4 식별합니다
        """
        pass    

    @abstractmethod
    def ob_image_mp4(self, binary: bytes):
        """
        mp4 식별합니다
        """
        pass
    
    @abstractmethod
    def ob_image_avi(self, binary: bytes):
        """
        avi 식별합니다
        """
        pass