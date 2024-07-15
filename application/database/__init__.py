import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from application.base_classes import CallableInstance
from application.database.bases import Base


class Database(CallableInstance):
    def __init__(self, db_uri: str) -> None:
        """This class encapsulates database configuration and
        initialization."""
        self.db_uri = db_uri
        self.engine = create_engine(url=db_uri)
        self.Session = sessionmaker(bind=self.engine, autoflush=True)
        self.Base = Base
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Database initialized")

    def initialize_tables(self) -> None:
        """Create the desired tables in the database if they don't already
        exist."""
        self.logger.info("Initializing all tables tables")
        self.Base.metadata.create_all(self.engine)

    def delete_tables(self) -> None:
        self.logger.info("Deleting all tables")
        self.Base.metadata.drop_all(self.engine)

    def truncate_db(self) -> None:
        self.logger.info("Cleaning database data")
        with self.Session() as session:
            # Allows truncating all schemas tables or just public schema
            table_names = ",".join([table.name for table in self.Base.metadata.sorted_tables])
            query = text(f"TRUNCATE {table_names} RESTART IDENTITY;")
            session.execute(query)
            session.commit()
