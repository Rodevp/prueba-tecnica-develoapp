from sqlalchemy import Column, Integer, String, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), default="active")  
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reservations")
    field = relationship("Field")