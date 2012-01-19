import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(cfg.sql_url, echo=False)
Session = sessionmaker(bind=engine)

