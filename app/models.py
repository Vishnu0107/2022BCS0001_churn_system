from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
from app.database import engine


Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    tenure = Column(Integer)
    monthly_charges = Column(Float)
    contract = Column(String)

Base.metadata.create_all(bind=engine)