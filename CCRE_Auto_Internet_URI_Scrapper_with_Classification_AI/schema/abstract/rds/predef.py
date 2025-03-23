from enum import Enum
from typing import TypedDict

class ConnectionAuthenticationFileType(Enum):
    """
    Allowed Connection Authentication Type definition
    """
    PEM = "cert"

class DatabaseType(Enum):
    """
    Allowed Database Type definition
    """
    SQLITE3 = "sqlite3"
    POSTGRESQL = "postgresql"
    # MYSQL = "mysql"
    # ORACLE = "oracle"
    
class ConnectionAuthenticationFileObject(TypedDict):
    """
    Type about connection authentication file
    """
    encrypted: str
    salt: str
    