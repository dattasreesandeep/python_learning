from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:root@localhost/company_fastapi"

engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

metadata = MetaData()