from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import DateTime, select, PoolProxiedConnection
from sqlalchemy.ext.hybrid import hybrid_property
import pytz

TIMEZONE = "utc"

Base = declarative_base()


class BaseCustomMeta(type(Base)):
    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        BaseCustomMeta.add_local_datetime_props(bases, cls, namespace)

        return cls

    @staticmethod
    def add_local_datetime_props(bases, cls, namespace):
        if Base not in bases:
            def decorator(local_name):
                def date_time_local(self):
                    if getattr(self, local_name).tzinfo is not None:
                        try:
                            return pytz.timezone(TIMEZONE).normalize(getattr(self, local_name))
                        except AttributeError as e:
                            return getattr(self, local_name).astimezone(pytz.timezone(TIMEZONE))
                    else:
                        return pytz.utc.localize(getattr(self, local_name)).astimezone(
                            pytz.timezone(TIMEZONE))

                return date_time_local

            vars_list = namespace.items()
            for name, attr in vars_list:
                if isinstance(getattr(attr, 'type', None), DateTime):
                    _datetime_local_prop = decorator(name)
                    _hybrid_datetime_local_prop = hybrid_property(_datetime_local_prop)
                    _expr_datetime_local_prop = _hybrid_datetime_local_prop.expression(_datetime_local_prop)
                    setattr(cls, f'{name}_local', _expr_datetime_local_prop)


class BaseCustom(Base, metaclass=BaseCustomMeta):
    __abstract__ = True


class PostgreSQL:
    def __init__(self):
        DATABASE_URL = "postgresql://admin:admin@localhost:5332/image_db"
        # Create the SQLAlchemy engine and session
        engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Base class for models
        BaseCustom.metadata.create_all(bind=engine)

    def get_db(self) -> Session:
        db = self.SessionLocal()
        try:
            return db
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            db.close()
            raise

