# migrate.py
import argparse
import os
from alembic.config import Config
from alembic import command

from typing import Callable, List, Optional, Protocol, Union
from alembic.script import ScriptDirectory

# Protocol을 사용한 함수 시그니처 정의
# 함수 파라미터와 일치시켜야 함.
class RunMigrationsProtocol(Protocol):
    def __call__(self, db_type: str, url: str, action: str, message: Optional[str] = None, revision: Optional[str] = None) -> None: ...

def run_migrations(db_type: str, url: str, action: str, message: str = None, revision: str = None) -> None:
    """지정된 데이터베이스에 대한 마이그레이션을 실행합니다.
    
    Args:
        db_type: The database type ('main' or 'local')
        url: Database connection URL
        action: Migration action to perform ('upgrade', 'revision', or 'downgrade')
        message: Migration message for revision
        revision: Specific revision identifier for downgrade (default: -1)
    """
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    alembic_ini_path = os.path.join(project_root, "CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI/alembic.ini")
    
    
    alembic_cfg = Config(alembic_ini_path)
    
    configuration = alembic_cfg.get_section(alembic_cfg.config_ini_section)
    configuration['sqlalchemy.url'] = url
    
    # 이상으로 필요한 것이 없다. 2개 이상 필요한 것이 있나?
    if db_type == "main":
        branch = "maindb"
    elif db_type == "local":
        branch = "localdb"
    else:
        print(f"Unknown database type: {db_type}")
        return
    
    # 버전을 업글하면 그게 전부다
    if action == "upgrade":
        command.upgrade(alembic_cfg, f"{branch}@head", tag=branch)  # tag 매개변수 추가
    elif action == "current":
        command.current(alembic_cfg, tag=branch)
    elif action == "revision":
        command.revision(alembic_cfg, autogenerate=True, message=message, branch_label=branch, tag=branch)  # tag 매개변수 추가
    elif action == "downgrade":
        rev = revision if revision else "-1"
        command.downgrade(alembic_cfg, f"{branch}@{rev}", tag=branch)  # tag 매개변수 추가
    elif action == "history":
        command.history(alembic_cfg, tag=branch)
    elif action == "stamp":
        command.stamp(alembic_cfg, f"{branch}@head", tag=branch)
    else:
        print(f"Unknown action: {action}")




def initialize_branch(db_type: str, url: str) -> bool:
    """
    Initialize a specific branch if it doesn't already exist.
    
    Args:
        db_type: Database type ('main' or 'local')
        url: Database connection URL
        
    Returns:
        bool: True if initialization was performed, False if already initialized
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    alembic_ini_path = os.path.join(project_root, "CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI/alembic.ini")
    
    alembic_cfg = Config(alembic_ini_path)
    configuration = alembic_cfg.get_section(alembic_cfg.config_ini_section)
    configuration['sqlalchemy.url'] = url
    
    if db_type == "main":
        branch = "maindb"
    elif db_type == "local":
        branch = "localdb"
    else:
        print(f"Unknown database type: {db_type}")
        return False
    
    # Check if branch is already initialized
    try:
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        revisions = list(script_dir.get_revisions(branch + "@head"))
        if revisions:
            print(f"Branch '{branch}' is already initialized")
            return False
    except Exception as e:
        # If we can't check revisions, likely not initialized
        pass
    
    # Initialize the branch
    command.revision(alembic_cfg, autogenerate=True, message=f"Initial {db_type} database", branch_label=branch)
    print(f"Initialized branch '{branch}'")
    return True

def init_migrations(db_type: str, url: str) -> None:
    """
    Initialize migrations for the specified database type.
    
    Args:
        db_type: Database type ('main', 'local', or 'all')
        url: Database connection URL
    """
    initialize_branch(db_type, url)






if __name__ == "__main__":
    """Manage database migrations using Alembic.
    
    Usage:
        python migrate.py --url <database_url> --db <main|local|all> --action <upgrade|revision> [--message <message>]
    """
    parser = argparse.ArgumentParser(description='Manage database migrations')
    parser.add_argument('--url', required=True, help='Database URL')
    parser.add_argument('--db', choices=['main', 'local', 'all'], required=True, help='Database to migrate')
    parser.add_argument('--action', choices=['upgrade', 'revision'], required=True, help='Migration action')
    parser.add_argument('--message', help='Migration message (for revision)')
    
    args = parser.parse_args()
    
    if args.db == 'all':
        run_migrations("main", args.url, args.action, args.message)
        run_migrations("local", args.url, args.action, args.message)
    else:
        run_migrations(args.db, args.url, args.action, args.message)