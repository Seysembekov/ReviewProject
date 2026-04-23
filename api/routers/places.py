from fastapi import APIRouter, status, HTTPException, Depends
from api.dependencies import get_redis_client, get_db_Session
from config import settings
from services.placeService import PlaceService
from schemes.places import PlaceResponse, CreatePlace
from sqlalchemy.orm import Session
from redis.asyncio import Redis
import json



app = APIRouter(prefix='/places', tags=['Places'])

@app.get('/')
async def get_all_places(db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = 'places:all'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = PlaceService(db)
    places = service.get_all()

    await redis.set(cache_key, json.dumps([p.model_dump() for p in places]), ex = settings.CACHE_EXPIRE)
    return places

@app.get('/{place_id}')
async def get_by_id(place_id: int, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = f'places:{place_id}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = PlaceService(db)
    place = service.get_by_id(place_id)

    await redis.set(cache_key, json.dumps(place.model_dump()), ex = settings.CACHE_EXPIRE)
    return place

@app.post('/')
async def create_place(data: CreatePlace, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    service = PlaceService(db)
    place = service.create_place(data)

    await redis.delete('places:all')
    return place

