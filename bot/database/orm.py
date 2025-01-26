import logging
import os

from dotenv import load_dotenv, find_dotenv

from sqlalchemy import String, create_engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class DatabaseManager(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    load_dotenv(find_dotenv())

    sync_engine = create_engine(
        os.getenv('DATABASE_URL'),
        echo=True
    )

    sync_session = sessionmaker(bind=sync_engine)

    @classmethod
    def create_tables(cls) -> bool | None:
        try:
            with cls.sync_engine.begin() as connection:
                cls.metadata.create_all(connection)
                return True
        except Exception as e:
            logging.error(f'Error in create_tables creating tables: {e}')
            return False

    @classmethod
    def insert_application(cls, **kwargs) -> bool | None:
        link = kwargs['link']
        try:
            with cls.sync_session() as session:
                instance = cls(link=link)
                session.add(instance)
                session.commit()
                return True
        except Exception as e:
            logging.error(f"Error in insert_application: {e}")
            return False

    @classmethod
    def get_applications(cls) -> list | None:
        try:
            with cls.sync_session() as session:
                applications = session.query(cls).all()
                return applications
        except Exception as e:
            logging.error(f"Error in get_applications: {e}")
            return None


class Application(DatabaseManager):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(255))

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'link': self.link
        }
