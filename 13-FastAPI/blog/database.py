from sqlaclhemy import create_engine
from sqlaclhemy.ext.declarative import declarative_base
from sqlaclhemy.orm import sessionmaker

SQLACLHEMY_DSN = 'postgresql:///.blog.db'

engine = create_engine(
    SQLACLHEMY_DSN,
    connect_args={
        'check_same_thread': False,
    }
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
