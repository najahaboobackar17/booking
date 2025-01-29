from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import auth
import models
from database import engine, SessionLocal

app = FastAPI()

# Include authentication router
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=200)
async def user(user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}

@app.get("/api/seats", response_model=List[bool])
async def fetch_available_seats(timeSlot: str, db: Session = Depends(get_db)):
    seats = db.query(models.Seats).filter(models.Seats.timeSlot == timeSlot).all()
    if not seats:
        raise HTTPException(status_code=404, detail="No seats available for this time slot")
    return [seat.isBooked for seat in seats]

@app.post("/api/seats/book")
async def book_seat(userId: str, timeSlot: str, seatNo: int, db: Session = Depends(get_db)):
    # Ensure the user has enough Blue Dollars before booking
    user = db.query(models.Users).filter(models.Users.id == userId).first()
    if user.blueDollars < 10:  # Assuming each seat costs 10 Blue Dollars
        raise HTTPException(status_code=400, detail="Insufficient Blue Dollars")
    
    # Check if seat is already booked
    seat = db.query(models.Seats).filter(models.Seats.timeSlot == timeSlot, models.Seats.seatNo == seatNo).first()
    if seat and seat.isBooked:
        raise HTTPException(status_code=400, detail="Seat is already booked")
    
    seat.isBooked = True
    seat.bookedBy = userId
    user.blueDollars -= 10  # Deduct Blue Dollars
    db.commit()

    ticket = models.Tickets(employeeId=userId, seatNo=seatNo, timeSlot=timeSlot)
    db.add(ticket)
    db.commit()
    
    return {"message": "Seat booked successfully", "ticket": ticket}
