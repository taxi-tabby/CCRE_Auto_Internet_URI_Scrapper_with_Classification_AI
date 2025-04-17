from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# Import models from your application
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import your models here - adjust the import path as needed
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models.base import Base, LocalBase

# Set the target metadata based on the current tag (which db we're working with)
current_tag = os.environ.get('ALEMBIC_TAG', None)
version_db_url = os.environ.get('ALEMBIC_VERSION_DB_URL', None)

# Choose the correct target metadata based on which database we're migrating
if current_tag == 'maindb':
    target_metadata = Base.metadata
elif current_tag == 'localdb':
    target_metadata = LocalBase.metadata
else:
    target_metadata = None

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    
    # Configure with appropriate target metadata and version table name
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Use a single version table for both databases, but with different entries
        # determined by the branch labels in the migration files
        version_table="alembic_version",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # For schema changes, use the primary URL from config
    schema_url = config.get_main_option("sqlalchemy.url")
    print(schema_url)
    connectable_schema = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=schema_url,
    )
    
    # For version tracking, use either the provided version DB URL or the same URL
    version_url = version_db_url if version_db_url else schema_url
    
    # Only use a separate engine for version tracking if a different URL was provided
    if version_url != schema_url:
        # Engine for version tracking (separate DB)
        connectable_version = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            url=version_url,
        )
        
        # Use the schema connection for actual migrations
        with connectable_schema.connect() as schema_conn, connectable_version.connect() as version_conn:
            # This is the key part: we use the version_conn for managing the 
            # alembic_version table, but schema_conn for actual schema changes
            context.configure(
                connection=schema_conn,
                target_metadata=target_metadata,
                version_table="alembic_version",
                version_table_connection=version_conn
            )
            
            with context.begin_transaction():
                context.run_migrations()
    else:
        # Using a single database for both schema and version tracking
        with connectable_schema.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                version_table="alembic_version",
            )
            
            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
