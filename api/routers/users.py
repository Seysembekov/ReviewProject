from schemes.users import UserResponse, CreateUser
from api.dependencies import get_redis_client, get_db_Session
from services.userService import UserService
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from redis.asyncio import Redis
import json
from config import settings

app = APIRouter(prefix = '/users', tags=['Users'])

@app.get('/', response_model=list[UserResponse])
async def get_all(db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = 'users:all'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = UserService(db)
    users = service.get_all()

    await redis.set(cache_key, json.dumps([u.model_dump() for u in users]), ex = settings.CACHE_EXPIRE)
    return users

@app.get('/id/{user_id}')
async def get_by_id(user_id: int, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = f'users:{user_id}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = UserService(db)
    user = service.get_by_id(user_id)

    await redis.set(cache_key, json.dumps(user.model_dump()), ex=settings.CACHE_EXPIRE)
    return user

@app.get('/username/{username}')
async def get_by_username(username: str, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = f'users:{username}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = UserService(db)
    user = service.get_by_username(username)
    await redis.set(cache_key, json.dumps(user.model_dump()), ex = settings.CACHE_EXPIRE)
    return user

@app.get('/favorites/{user_id}')
async def get_favorites(user_id: int, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = f'users:favorites:{user_id}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = UserService(db)
    favorites = service.get_favorites(user_id)
    await redis.set(cache_key, json.dumps([f.model_dump() for f in favorites]), ex=settings.CACHE_EXPIRE)
    return favorites

@app.post('/add-favorite/{user_id}')
async def add_favorite(user_id: int, place_id: int = Query(...), db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    service = UserService(db)
    favorite = service.add_favorite(user_id, place_id)

    await redis.delete(f'users:favorites:{user_id}')
    return favorite

@app.delete('/favorites/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(user_id: int, place_id: int = Query(...), db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    service = UserService(db)

    service.remove_from_favorite(user_id, place_id)

    await redis.delete(f'users:favorites:{user_id}')

@app.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUser, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    service = UserService(db)
    user = service.create_user(data)

    await redis.delete('users:all')

    return user

