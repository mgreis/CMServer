from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

server = 'localhost:3306'
db = 'sqlalchemy'
login = 'root'
password = '12345678'


engine_str = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(login,password,server,db)
engine = create_engine(engine_str, echo = True, encoding = 'utf8')

db_session = scoped_session(sessionmaker(autocommit = False,
                                    autoflush = False,
                                    bind = engine))
Base = declarative_base()
Base.query = db_session.query_property()




def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    return db_session