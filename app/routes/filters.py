from typing import List, Optional

from fastapi import APIRouter, Query, Depends
from sqlalchemy import select

from ..db import Item, AsyncDB
from ..schemas import ItemResponse


filters_router = APIRouter(prefix="/filter", tags=["Filters"])

@filters_router.get("/items", response_model=List[ItemResponse])
async def get_filtered_items(
    title: Optional[str] = Query(None, max_length=100),
    category: Optional[str] = Query(None, max_length=50),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    session = Depends(AsyncDB.get_session)
):
    query = select(Item)  
    if title:
        query = query.where(Item.title.ilike(f"%{title}%"))
    if category:
        query = query.where(Item.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.where(Item.price >= min_price)
    if max_price is not None:
        query = query.where(Item.price <= max_price)
    result = await session.scalars(query)  
    return result.all()
