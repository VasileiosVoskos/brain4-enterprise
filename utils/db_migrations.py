from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    try:
        engine = create_engine(DATABASE_URL)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Add new tables or columns here
        # Example:
        # if 'new_table' not in metadata.tables:
        #     engine.execute('CREATE TABLE new_table (id INTEGER PRIMARY KEY, name TEXT)')
        
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        raise

if __name__ == "__main__":
    run_migrations()
