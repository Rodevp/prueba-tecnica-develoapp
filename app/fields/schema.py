from pydantic import BaseModel, Field


class FieldCreate(BaseModel):
    name: str = Field(..., example="Cancha 1")
    description: str | None = Field(None, example="Cancha de césped sintético")
    price_per_hour: float = Field(..., example=50.0)
    location: str = Field(..., example="Calle 123")
    capacity: int = Field(..., example=10)


class FieldUpdate(BaseModel):
    name: str | None = Field(None, example="Cancha A")
    description: str | None = Field(None, example="Renovada en 2024")
    price_per_hour: float | None = Field(None, example=60.0)
    location: str | None = Field(None, example="Calle 123")
    capacity: int | None = Field(None, example=10)

