from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
from .config import DATABASE_URL

Base = declarative_base()

class Claim(Base):
    __tablename__ = 'claims'
    
    id = Column(Integer, primary_key=True)
    claim_id = Column(String, unique=True)
    date = Column(DateTime)
    amount = Column(Float)
    status = Column(String)
    type = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), onupdate=lambda: datetime.now(pytz.UTC))

class LegalCase(Base):
    __tablename__ = 'legal_cases'
    
    id = Column(Integer, primary_key=True)
    case_id = Column(String, unique=True)
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC), onupdate=lambda: datetime.now(pytz.UTC))

# Initialize database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return Session()
