from fastapi import FastAPI

from src.clients.endpoints.router import client_router
from src.users.endpoints.router import users_router
from src.profiles.endpoints.router import profile_router
from src.vehicles.endpoints.router import vehicles_router

app = FastAPI()

app.include_router(client_router)
app.include_router(users_router)
app.include_router(profile_router)
app.include_router(vehicles_router)
