from fastapi import FastAPI
from .routes import auth_router, items_router, filters_router, chat


app = FastAPI()


app.include_router(auth_router)
app.include_router(items_router)
app.include_router(filters_router)