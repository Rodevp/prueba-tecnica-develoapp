from pydantic import BaseModel
from typing import List

class FieldStats(BaseModel):
    field: str
    total: int

class ReservationStats(BaseModel):
    actives: int
    cancels: int
    total: int

class UsersStats(BaseModel):
    total: int


class AdminStatsResponse(BaseModel):
    reservation_per_field: List[FieldStats]
    reservations: ReservationStats
    users: UsersStats
