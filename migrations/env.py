import sys
import os
import sqlmodel
from sqlmodel import SQLModel
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()  

from events_app_backend.users.models import User
from events_app_backend.roles.models import Role
from events_app_backend.events.models import Event, EventStatus, Session
from events_app_backend.registrations.models import EventRegistration

target_metadata = SQLModel.metadata

config = context.config

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("No se encontró DATABASE_URL en las variables de entorno")

config.set_main_option("sqlalchemy.url", database_url)
# config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
