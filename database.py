from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base #doubt

SQLALCHEMY_DATABASE_URL="sqlite:///./recipe.db"
# SQLALCHEMY_DATABASE_URL="postgresql://supeusrname:password@localhost/databasename"
# SQLALCHEMY_DATABASE_URL="mysql+pymysql://"usrname:password@url:port/databasename"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
    # SQLALCHEMY_DATABASE_URL for postgresql same for mysql

)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()


