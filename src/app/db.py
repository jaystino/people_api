import os

from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import func

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
persons = Table(
    "persons",
    metadata,
    Column("record", Integer, primary_key=True),
    Column("id", UUID(as_uuid=True), nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("middle_name", String(50)),
    Column("last_name", String(50), nullable=False),
    Column("email", String(50), nullable=False),
    Column("age", Integer, nullable=False),
    Column("version", Integer, default=1, nullable=False),
    Column("is_latest", Boolean, default=True, nullable=False),
    Column("created_date", DateTime, default=func.now(), nullable=False),
    UniqueConstraint("id", "version", name="id_version_uc"),
)

# databases query builder
database = Database(DATABASE_URL)
