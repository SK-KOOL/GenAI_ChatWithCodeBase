from sqlalchemy import create_engine

DB_URL = "mysql+pymysql://root:root@localhost/testdb"

engine = create_engine(DB_URL)