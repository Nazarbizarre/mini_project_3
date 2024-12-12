from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select


from ..schemas import Advertisement
from ..db import AsyncDB, Item, User
from ..utils import get_current_user


items_router = APIRouter(prefix="/item", tags=['Item'])



@items_router.get("/")
def read_root():
    return {"hello" : "world"}



@items_router.post("/create", status_code = status.HTTP_201_CREATED)
def create_item(data: Advertisement,
                current_user: Annotated[User, Depends(get_current_user)],
                session = Depends(AsyncDB.get_session)):
    item = Item(**data.model_dump(), name=current_user)
    session.add(item)



@items_router.get("/{item_id}")
def item_info(item_id: int, session = Depends(AsyncDB.get_session)):
    item = session.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(
            detail = f"Item with id {item_id} not found",
            status_code = status.HTTP_404_NOT_FOUND
        )
    else:
        return item

    
@items_router.delete("/delete{item_id}")
def delete_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session = Depends(AsyncDB.get_session)
):
    item = session.scalar((Item).where(Item.id == item_id))
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.author_id != current_user.id:
                raise HTTPException(
            status_code=403, detail="Not authorized to delete this item"
        )
        
    session.delete(item)
    return item
        
    
    
@items_router.get("/all")
def get_all_items(session = Depends(AsyncDB.get_session)):
    items = session.scalars(select(Item))
    return items

    
    
    


