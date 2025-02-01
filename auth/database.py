import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



# Retrieve environment variables
postgres_host = os.environ.get("POSTGRES_HOST")
postgres_db = os.environ.get("POSTGRES_DB")
postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")


# Assuming your PostgreSQL server is running locally with a database named 'mydatabase'
DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"

class connect_orm:
    def __init__(self):
        self.engine = _sql.create_engine(DATABASE_URL)
        self.SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = _declarative.declarative_base()
