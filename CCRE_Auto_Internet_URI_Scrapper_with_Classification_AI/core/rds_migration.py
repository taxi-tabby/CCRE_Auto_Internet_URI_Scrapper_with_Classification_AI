from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from sqlalchemy.exc import SQLAlchemyError


def _chk_rds_table_exists(db: Session, db_type: DatabaseType, table_name: str) -> bool:
    """
    Check if the table exists in the database.
    """
    try:
        with db:
            
            if db_type == DatabaseType.POSTGRESQL:
                result = db.execute(f"SELECT to_regclass('{table_name}')")
                return bool(result.scalar())
            
            
            
            elif db_type == DatabaseType.MYSQL:
                query = f"SHOW TABLES LIKE '{table_name}'"
                result = db.execute(query)
                return result.fetchone() is not None
            
            
            
            elif db_type == DatabaseType.SQLITE3:
                query = text(f"SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name")
                result = db.execute(query, {"table_name": table_name})
                return result.fetchone() is not None
            
            
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
            
    except SQLAlchemyError as e:
        # SQLAlchemyError를 잡아서 구체적인 오류 메시지를 출력
        print(f"SQLAlchemyError occurred: {str(e)}")
        return False
    
    except Exception as e:
        # 예외 메시지 출력 시, 실제 예외 객체의 내용을 출력합니다.
        print(f"Error occurred: {str(e)}")
        return False
    
    
def table_init(engine: Engine, db: Session, db_type: DatabaseType):
    """
    Initialize the table.
    """
    if not _chk_rds_table_exists(db, db_type, "roots"):
        Roots.metadata.create_all(engine) 
   
    if not _chk_rds_table_exists(db, db_type, "branches"):
        Branches.metadata.create_all(engine) 
   
    if not _chk_rds_table_exists(db, db_type, "leaves"):
        Leaves.metadata.create_all(engine) 