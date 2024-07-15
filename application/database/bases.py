from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: type[DeclarativeMeta] = declarative_base()
