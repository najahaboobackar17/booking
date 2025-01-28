from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Correct PostgreSQL connection URL (ensure password is properly encoded)
DATABASE_URL = 'postgresql://postgres:Najah%40123@localhost:5432/booking'

# Create engine without 'check_same_thread'
engine = create_engine(DATABASE_URL)

# SessionLocal setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base setup for models
Base = declarative_base()
