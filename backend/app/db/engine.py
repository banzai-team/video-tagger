from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import DATABASE_URL
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database engine created successfully")
except SQLAlchemyError as e:
    logger.error(f"Error creating database engine: {str(e)}")
    raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test database connection
def test_db_connection():
    try:
        with engine.connect() as connection:
            logger.info("Successfully connected to the database")
    except SQLAlchemyError as e:
        logger.error(f"Error connecting to the database: {str(e)}")
        raise


# Call the test function
test_db_connection()
