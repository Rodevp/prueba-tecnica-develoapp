from pydantic import BaseModel, Field
from datetime import datetime


class ReservationCreate(BaseModel):
    field_id: int = Field(..., example=1)
    start_time: datetime = Field(..., example="2025-05-20T14:00:00")
    end_time: datetime = Field(..., example="2025-05-20T15:00:00")
