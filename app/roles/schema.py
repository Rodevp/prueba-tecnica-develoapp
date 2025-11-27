from pydantic import BaseModel, Field
from typing import List

class RoleCreate(BaseModel):
    name: str = Field(..., example="admin")
    description: str | None = Field(None, example="Administrador del sistema")
    permissions: List[str] = Field(default_factory=list, example=["fields:create", "dashboard:view"])

class AssingRole(BaseModel):
    user_id: int = Field(..., example=1)
    role_id: int = Field(..., example=1)

class RoleResponse(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="admin")
    description: str | None = Field(None, example="Administrador del sistema")
    permissions: List[str] = Field(default_factory=list, example=["fields:create", "dashboard:view"])