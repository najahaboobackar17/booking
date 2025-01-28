from fastapi import FastAPI ,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
import models
from database import engine ,SessionLocal
from sqlalchemy.orm import Session
import auth

app=FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependancy=Annotated[Session,Depends(get_db)]

@app.get("/",status_code=200)
async def user(user:None,db:db_dependancy):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    return {"User":user}
