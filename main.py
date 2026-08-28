from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

import models
import schemas

from database import engine, get_db


# Create database tables
models.Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Tiwari Sai Dental API",
    description="Appointment Management System",
    version="1.0"
)


# -----------------------------
# SERVE STATIC FILES
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# -----------------------------
# HOME PAGE
# -----------------------------

@app.get("/")
def home():
    return FileResponse("static/index.html")


# -----------------------------
# CREATE APPOINTMENT
# -----------------------------

@app.post(
    "/appointments",
    response_model=schemas.AppointmentResponse
)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):

    new_appointment = models.Appointment(
        name=appointment.name,
        phone=appointment.phone,
        service=appointment.service,
        location=appointment.location,
        message=appointment.message
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# -----------------------------
# GET ALL APPOINTMENTS
# -----------------------------

@app.get(
    "/appointments",
    response_model=List[schemas.AppointmentResponse]
)
def get_appointments(
    db: Session = Depends(get_db)
):

    appointments = (
        db.query(models.Appointment)
        .order_by(models.Appointment.id.desc())
        .all()
    )

    return appointments


# -----------------------------
# UPDATE APPOINTMENT STATUS
# -----------------------------

@app.put(
    "/appointments/{appointment_id}/status",
    response_model=schemas.AppointmentResponse
)
def update_status(
    appointment_id: int,
    status_data: schemas.AppointmentStatusUpdate,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = status_data.status

    db.commit()
    db.refresh(appointment)

    return appointment


# -----------------------------
# DELETE APPOINTMENT
# -----------------------------

@app.delete("/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }