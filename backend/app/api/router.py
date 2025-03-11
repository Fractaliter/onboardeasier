from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.item import ItemCreate, ItemRead
from app.crud.item import create_item, get_items, delete_item

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items/", response_model=ItemRead)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db=db, item=item)

@router.get("/items/", response_model=list[ItemRead])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_items(db=db, skip=skip, limit=limit)

@router.delete("/items/{item_id}", response_model=ItemRead)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db=db, item_id=item_id)
