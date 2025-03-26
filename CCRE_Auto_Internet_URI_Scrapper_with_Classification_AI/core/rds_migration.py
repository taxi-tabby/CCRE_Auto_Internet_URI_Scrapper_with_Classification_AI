from sqlalchemy.orm import Session
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType




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
                result = db.execute(f"SHOW TABLES LIKE '{table_name}'")
                return result.fetchone() is not None
            elif db_type == DatabaseType.SQLITE:
                result = db.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                return result.fetchone() is not None
            else:
                raise ValueError(f"Unsupported database type: {db_type}")
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    
def _table_init(db: Session, db_type: DatabaseType):
    """
    Initialize the table.
    """
    if not _chk_rds_table_exists(db, db_type, "ccre_roots"):
       # 추후 모델 생성하고 테이블 추가할 것
       pass 