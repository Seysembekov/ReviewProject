from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from redis.asyncio import Redis
from api.dependencies import get_redis_client, get_db_Session, get_current_user
from services.reviewsService import ReviewService
from schemes.reviews import ReviewResponse, CreateReview
import json
from config import settings

app = APIRouter(prefix='/reviews', tags=['Reviews'])

@app.get('/')
async def get_all(offset: int = 0, limit: int = 20, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = 'reviews:all'
    cached =await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = ReviewService(db)
    reviews = service.get_all(offset, limit)

    await redis.set(cache_key, json.dumps([r.model_dump() for r in reviews]), ex = settings.CACHE_EXPIRE)
    return reviews

@app.get('/by-user/{user_id}')
async def get_by_user(user_id: int, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = f'reviews:users:{user_id}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = ReviewService(db)
    reviews = service.get_by_user(user_id)

    await redis.set(cache_key, json.dumps([r.model_dump() for r in reviews]), ex = settings.CACHE_EXPIRE)
    return reviews

@app.get('/by-place/{place_id}')
async def get_by_place(place_id: int, db: Session = Depends(get_db_Session), redis: Redis = Depends(get_redis_client)):
    cache_key = f'reviews:places:{place_id}'
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    service = ReviewService(db)
    reviews = service.get_by_place(place_id)

    await redis.set(cache_key, json.dumps([r.model_dump() for r in reviews]), ex = settings.CACHE_EXPIRE)
    return reviews

@app.post('/')
async def create_review(data: CreateReview,
                        db: Session = Depends(get_db_Session),
                        redis: Redis = Depends(get_redis_client),
                        current_user: int = Depends(get_current_user)):

    service = ReviewService(db)
    review = service.create_review(data, current_user)

    await redis.delete('reviews:all')
    await redis.delete(f'reviews:users:{current_user}')
    await redis.delete(f'reviews:places:{data.review_on_place}')
    return review



