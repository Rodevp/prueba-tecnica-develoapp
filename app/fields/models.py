from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_hour = Column(Float, nullable=False)