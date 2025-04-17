# migrate.py
import argparse
import os
from alembic.config import Config
from alembic import command

from typing import Callable, List, Optional, Protocol, Union
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

# Protocol을 사용한 함수 시그니처 정의
class RunMigrationsProtocol(Protocol):
    def __call__(self, db_type: str, schema_url: str, action: str, message: Optional[str] = None, 
                revision: Optional[str] = None, version_url: Optional[str] = None) -> None: ...


def run_migrations(db_type: str, schema_url: str, action: str, message: str = None, revision: str = None, 
                  version_url: str = None) -> None:
    """지정된 데이터베이스에 대한 마이그레이션을 실행합니다.
    
    Args:
        db_type: The database type ('main' or 'local')
        schema_url: Database connection URL for schema changes
        action: Migration action to perform ('upgrade', 'revision', 'downgrade', 'history', 'stamp')
        message: Migration message for revision
        revision: Specific revision identifier for downgrade (default: -1)
        version_url: Database URL for version tracking (main db by default)
    """
    
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 프로젝트 루트 디렉토리 경로 (core 폴더의 상위 디렉토리)
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # 알엠빅 설정 파일 경로
    alembic_ini_path = os.path.join(project_root, "CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI/alembic.ini")
    
    # 알엠빅 설정 파일이 없으면 에러 메시지 출력
    if not os.path.exists(alembic_ini_path):
        print(f"Error: alembic.ini not found at {alembic_ini_path}")
        return
    
    alembic_cfg = Config(alembic_ini_path)
    
    # 스키마 URL 설정 (실제 마이그레이션 변경에 사용)
    configuration = alembic_cfg.get_section(alembic_cfg.config_ini_section)
    configuration['sqlalchemy.url'] = schema_url
    
    # 브랜치 설정
    if db_type == "main":
        branch = "maindb"
    elif db_type == "local":
        branch = "localdb"
    else:
        print(f"Unknown database type: {db_type}")
        return
    
    # 환경 변수를 통해 태그 전달
    os.environ['ALEMBIC_TAG'] = branch
    
    # 버전 추적을 위한 URL이 별도로 제공된 경우
    if version_url:
        os.environ['ALEMBIC_VERSION_DB_URL'] = version_url
    
    try:
        # 마이그레이션 액션 실행
        if action == "upgrade":
            command.upgrade(alembic_cfg, f"{branch}@head")
        elif action == "revision":
            if not message:
                message = f'init {branch} db'
            command.revision(alembic_cfg, autogenerate=True, message=message, branch_label=branch)
        elif action == "downgrade":
            rev = revision if revision else "-1"
            command.downgrade(alembic_cfg, f"{branch}@{rev}")
        elif action == "history":
            command.history(alembic_cfg)
        elif action == "stamp":
            command.stamp(alembic_cfg, f"{branch}@head")
        elif action == "init":
            # Initialize both databases with the same version tracking
            command.init(alembic_cfg, "migrations")
        else:
            print(f"Unknown action: {action}")
    finally:
        # 환경 변수 정리
        if 'ALEMBIC_TAG' in os.environ:
            del os.environ['ALEMBIC_TAG']
        if 'ALEMBIC_VERSION_DB_URL' in os.environ and version_url:
            del os.environ['ALEMBIC_VERSION_DB_URL']


if __name__ == "__main__":
    """Manage database migrations using Alembic.
    
    Usage:
        python migrate.py --schema-url <schema_db_url> --db <main|local|all> --action <action> 
                         [--message <message>] [--revision <revision>] [--version-url <version_db_url>]
    """
    parser = argparse.ArgumentParser(description='Manage database migrations')
    parser.add_argument('--schema-url', required=True, help='Database URL for schema changes')
    parser.add_argument('--db', choices=['main', 'local', 'all'], required=True, help='Database to migrate')
    parser.add_argument('--action', choices=['upgrade', 'revision', 'downgrade', 'history', 'stamp', 'init'], 
                       required=True, help='Migration action')
    parser.add_argument('--message', help='Migration message (for revision)')
    parser.add_argument('--revision', help='Revision identifier (for downgrade)')
    parser.add_argument('--version-url', help='Database URL for version tracking (defaults to main db url)')
    
    args = parser.parse_args()
    
    if args.db == 'all':
        run_migrations("main", args.schema_url, args.action, args.message, args.revision, args.version_url)
        run_migrations("local", args.schema_url, args.action, args.message, args.revision, args.version_url)
    else:
        run_migrations(args.db, args.schema_url, args.action, args.message, args.revision, args.version_url)