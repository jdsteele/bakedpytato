import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(cfg.sql_url, echo=False)
Session = sessionmaker(bind=engine, autocommit=False)

def remote_engine():
	return create_engine(cfg.sql_remote_url, echo=False)
