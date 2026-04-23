from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from redis_client import redis_client

from api.routers import auth, users, places , reviews

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print('DataBase Table created')

    await redis_client.ping()
    print('redis connected')
    yield
    await redis_client.aclose()
    print('redis connection closed')

app = FastAPI(
    title='Reviews on places API',
    version='0.0.1',
    lifespan = lifespan
)

app.include_router(auth.app, prefix='/api/v1')
app.include_router(users.app, prefix='/api/v1')
app.include_router(places.app, prefix='/api/v1')
app.include_router(reviews.app, prefix='/api/v1')

@app.get('/health', tags=['System'])
def health():
    return {'status' : 'ok'}