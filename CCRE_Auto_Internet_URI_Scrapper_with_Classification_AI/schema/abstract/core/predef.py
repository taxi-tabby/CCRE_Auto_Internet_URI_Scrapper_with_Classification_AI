from enum import Enum
from typing import TypedDict



class RootMessageQueueType(Enum):
    """
    ### (최상위 메세지 큐 동작)
    루트에서의 큐 동작 종류
    """
    UPLOAD = "upload"
    
class BranchMessageQueueType(RootMessageQueueType):
    """
    
    ### (RootMessageQueueType enum 에서 상속됨)
    브랜치에서의 큐 동작 종류 
    """
    EXPLORE = "explore"
    
    


# class ConnectionAuthenticationFileObject(TypedDict):
#     """
#     Type about connection authentication file
#     """
#     encrypted: str
#     salt: str
    