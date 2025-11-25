from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

from app.auth.routers import router as auth_router
from app.roles.routers import router as roles_router
from app.fields.routers import router as fields_router
from app.reservations.routers import router as reservations_router
from app.admin.routers import router as admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Soccer Field Reservation API",
    version="1.0.0",
    description="Sistema modular para gestionar reservas de canchas con roles, permisos y dashboard."
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(fields_router)
app.include_router(reservations_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Soccer Reservation API is running!",
        "status": "ok"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, debug=True)