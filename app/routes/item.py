from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select, update


from ..schemas import Advertisement, UpdateItemSchema, ItemResponse
from ..db import AsyncDB, Item, User
from ..utils import get_current_user


items_router = APIRouter(prefix="/item", tags=["Item"])


@items_router.get("/")
def read_root():
    return {"hello": "world"}


@items_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_item(
    data: Advertisement,
    current_user: Annotated[User, Depends(get_current_user)],
    session=Depends(AsyncDB.get_session),
):
    item = Item(**data.model_dump(), author_id=current_user.id, author = current_user.name)
    session.add(item)
    return "Item Created"


@items_router.get("/{item_id}", response_model=ItemResponse)
async def item_info(item_id: int, session=Depends(AsyncDB.get_session)):
    item = await session.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(
            detail=f"Item with id {item_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    else:
        return item


@items_router.delete("/delete/{item_id}")
async def delete_item(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session=Depends(AsyncDB.get_session),
):
    item = await session.scalar(select(Item).where(Item.id == item_id))

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this item"
        )

    await session.delete(item)
    return "Item Deleted"


@items_router.get("/items/all", response_model=List[ItemResponse])
async def get_all_items(session=Depends(AsyncDB.get_session)):
    items = await session.scalars(select(Item))
    items_response = [ItemResponse(**item.__dict__) for item in items]
    return items_response


@items_router.put("/update/{item_id}")
async def update_item(
    item_id: int,
    data: UpdateItemSchema,  
    current_user: Annotated[User, Depends(get_current_user)],
    session = Depends(AsyncDB.get_session),
):
    item = await session.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    
    upd = update(Item).where(Item.id == item_id).values(
        title=data.title or item.title,
        description=data.description or item.description,
        price=data.price if data.price is not None else item.price,
        category=data.category or item.category
    )
    await session.execute(upd)
    return {"detail": "Item updated"}