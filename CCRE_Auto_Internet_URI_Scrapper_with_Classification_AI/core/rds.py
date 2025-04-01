from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.helper.stringify.json import stringify_to_json
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.abstract.rds.predef import DatabaseType
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models import *
from sqlalchemy.exc import SQLAlchemyError

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.scrapper_root import Scrapper_Root


"""
RDS 동작 모음.
따로 mvc 어찌고 뭐시기 패턴을 쓸 이유가 없다.
목적에 맞게 씁시다 사람들아. 
과한 정리 개념은 오히려 코드를 복잡하게 만들어
"""













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
    없으면 테이블 생성. 
    create_all 에서 별도로 동작하나 그냥 쿼리로 체크함.
     
    @TODO: 불필요한 더블체크 있으니 수정할 것. (create_all 메서드 동작에 대해 검증하지 않았음으로 기능이 들어감) 
    """
    if not _chk_rds_table_exists(db, db_type, "roots"):
        Roots.metadata.create_all(engine) 
   
    if not _chk_rds_table_exists(db, db_type, "branches"):
        Branches.metadata.create_all(engine) 
   
    if not _chk_rds_table_exists(db, db_type, "leaves"):
        Leaves.metadata.create_all(engine) 
        
        
        
def update_roots(db: Session, roots: list[Scrapper_Root]):
    """
    roots 리스트를 순회하며 root_key가 없는 경우 새로 등록하고,
    이미 존재하는 경우 정보를 업데이트합니다.
    """
    try:
        with db.begin():  # 트랜잭션 시작
            for root in roots:
                # 기존 root_key가 존재하는지 확인
                existing_root = db.query(Roots).filter_by(root_key=root.root_key).first()
                
                if existing_root:
                    # 기존 root 업데이트
                    existing_root.root_uri = root.root_uri
                    existing_root.rules = root.access_rule.to_json()
                    # print(f'root updated: {root.root_key}')
                else:
                    # 새로운 root 추가
                    new_root = Roots(root_key=root.root_key, root_uri=root.root_uri, rules=root.access_rule.to_json())
                    db.add(new_root)
                    # print(f'new root added: {root.root_key}')
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
            

def get_roots_list(db: Session, page: int = 1, block: int = 10) -> list[Roots]:
    """
    루트 목록을 얻음 (기본 페이징 형식)
    Continuously request 기법을 통해 전체 목록을 가져올 수고 있고
    block 을 매우 높게 하여 한번에 얻을 수도 있음.
    """
    return db.query(Roots).offset((page - 1) * block).limit(block).all()



def get_root_branch_count(db: Session, root_id: int) -> int:
    """
    루트에 연결된 브랜치 수를 반환
    """
    return db.query(Branches).filter_by(root_id = root_id).count()
        
        
def get_exists_branch(db: Session, root_id: int, branch_uri: str) -> bool:
    """
    루트에 해당하는 브랜치가 존재하는지 확인
    """
    return db.query(Branches).filter_by(root_id=root_id, branch_uri=branch_uri).first() is not None

def get_branch_id_if_exists(db: Session, root_id: int, branch_uri: str) -> int | None:
    """
    루트에 해당하는 브랜치가 존재하면 branch의 id를 반환하고,
    존재하지 않으면 None을 반환
    """
    branch = db.query(Branches).filter_by(root_id=root_id, branch_uri=branch_uri).first()
    return branch.id if branch else None


def update_branches(db: Session, branches: list[Branches]) -> list[int]:
    """
    branches 리스트를 순회하며 branch_uri가 없는 경우 새로 등록하고,
    이미 존재하는 경우 변경사항이 있으면 업데이트합니다.
    생성된 branch의 id를 반환합니다.
    """
    created_ids = []
    try:
        with db.begin():  # 트랜잭션 시작
            for branch in branches:
                # 기존 branch_uri가 존재하는지 확인
                existing_branch = db.query(Branches).filter_by(branch_uri=branch.branch_uri).first()
                
                if existing_branch:
                    # 변경사항이 있는 경우에만 업데이트
                    if existing_branch.root_id != branch.root_id:
                        existing_branch.root_id = branch.root_id
                        
                else:
                    # 새로운 branch 추가
                    new_branch = Branches(root_id=branch.root_id, parent_id=branch.parent_id, branch_uri=branch.branch_uri)
                    db.add(new_branch)
                    db.flush()  # 새로 추가된 객체의 id를 가져오기 위해 flush 호출
                    created_ids.append(new_branch.id)
                    
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
    
    return created_ids