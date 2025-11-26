from pydantic import BaseModel
from typing import List

class FieldStats(BaseModel):
    field: str
    total: int


class ReservationStats(BaseModel):
    activas: int
    canceladas: int
    total: int


class UsersStats(BaseModel):
    total: int


class AdminStatsResponse(BaseModel):
    reservas_por_cancha: List[FieldStats]
    reservas: ReservationStats
    usuarios: UsersStats
