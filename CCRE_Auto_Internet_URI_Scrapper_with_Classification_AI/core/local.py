from datetime import datetime, timedelta, timezone
from typing import Optional
import pytz
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.stringify.json import stringify_to_json
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from sqlalchemy.exc import SQLAlchemyError

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root


"""
LOCAL RDS 동작 모음.
"""











def _chk_rds_table_exists(db: Session, db_type: DatabaseType, table_name: str) -> bool:
    """
    Check if the table exists in the database.
    """
    try:
        with db:
            
            if db_type == DatabaseType.POSTGRESQL:
                # 'text()'로 SQL 문을 감싸줍니다
                result = db.execute(text(f"SELECT to_regclass('{table_name}')"))
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
        print(f"SQLAlchemyError occurred: {e}")
        return False
    
    except Exception as e:
        # 예외 메시지 출력 시, 실제 예외 객체의 내용을 출력합니다.
        print(f"Error occurred: {e}")
        return False
    
    
def table_init(engine: Engine, db: Session, db_type: DatabaseType):
    """
    없으면 테이블 생성. 
    create_all 에서 별도로 동작하나 그냥 쿼리로 체크함.
     
    @TODO: 불필요한 더블체크 있으니 수정할 것. (create_all 메서드 동작에 대해 검증하지 않았음으로 기능이 들어감) 
    """
    if not _chk_rds_table_exists(db, db_type, "local_profile"):
        LocalProfile.metadata.create_all(engine)
   
  
def save_local_profile(db: Session, data_key: str, data_value: str) -> int:
    """
    로컬 프로필에 키-값 쌍을 저장합니다.
    동일한 키가 있어도 새 레코드로 계속 추가됩니다.
    
    Args:
        db (Session): 데이터베이스 세션
        data_key (str): 데이터 키
        data_value (str): 데이터 값
        
    Returns:
        int: 생성된 레코드의 ID, 오류 발생 시 -1
    """
    val_id = -1
    
    try:
        with db.begin():  # 트랜잭션 시작
            new_profile = LocalProfile(data_key=data_key, data_value=data_value)
            db.add(new_profile)
            db.flush()  # ID를 얻기 위해 flush 호출
            val_id = new_profile.id
            
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
    finally:
        try:
            db.commit()
        except Exception as e:
            print(f"Commit failed: {str(e)}")
            db.rollback()
    
    return val_id
  
  
def get_latest_local_profile(db: Session, data_key: str) -> Optional[str]:
    """
    주어진 키에 대한 가장 최근 값을 반환합니다.
    
    Args:
        db (Session): 데이터베이스 세션
        data_key (str): 조회할 데이터 키
        
    Returns:
        Optional[str]: 키에 해당하는 가장 최근 값, 없으면 None
    """
    try:
        # 생성 날짜를 기준으로 내림차순 정렬하여 첫 번째 항목 가져오기
        profile = db.query(LocalProfile).filter_by(data_key=data_key).order_by(
            LocalProfile.created_at.desc()
        ).first()
        
        return profile.data_value if profile else None
        
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None




