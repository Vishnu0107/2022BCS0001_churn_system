from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import time
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if "postgresql" in DB_URL:
    for i in range(10):
        try:
            engine = create_engine(DB_URL)
            connection = engine.connect()
            print("Connected to DB")
            break
        except Exception:
            print("⏳ Waiting for DB...")
            time.sleep(2)
    else:
        raise Exception("Could not connect to DB")
else:
    engine = create_engine(
        DB_URL,
        connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)