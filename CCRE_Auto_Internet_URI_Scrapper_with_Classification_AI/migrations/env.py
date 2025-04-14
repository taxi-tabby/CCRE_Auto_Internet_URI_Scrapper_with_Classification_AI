from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models.base import Base, LocalBase

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

# 현재 브랜치에 맞는 메타데이터 선택
def get_metadata_for_branch():
    """현재 실행 중인 브랜치에 맞는 메타데이터 반환"""
    # 브랜치 레이블 확인
    branch_labels = context.get_tag_argument() or ""
    if 'localdb' in branch_labels:
        print("Using LocalBase metadata for localdb branch")
        return LocalBase.metadata
    else:
        print("Using Base metadata for maindb branch")
        return Base.metadata

# 메타데이터 설정 - 이 부분이 중요합니다!
target_metadata = get_metadata_for_branch()

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    
    tag_argument = context.get_tag_argument() or ""
    version_table = "alembic_version_local" if "localdb" in tag_argument else "alembic_version_main"
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table=version_table,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # tag_argument 변수를 한 번만 설정하고 재사용
        tag_argument = context.get_tag_argument() or ""
        version_table = "alembic_version_local" if "localdb" in tag_argument else "alembic_version_main"
        
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            version_table=version_table,
        )

        with context.begin_transaction():
            context.run_migrations()




if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
