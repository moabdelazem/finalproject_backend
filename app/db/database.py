from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./db.sqlite3"

# Create a new database engine
engine = create_engine(DATABASE_URL)
# Create a new sessionmaker object
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """
    Creates database tables based on the defined models.

    This function uses the `create_all` method from SQLAlchemy's `Base.metadata` object
    to create all the tables defined in the database engine.

    """
    Base.metadata.create_all(bind=engine)


# Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
