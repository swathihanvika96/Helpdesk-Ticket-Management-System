from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import engine, get_db
from auth import (
    verify_password,
    create_access_token
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# REGISTER

@app.post("/register")
def register(
        user: schemas.UserRegister,
        db: Session = Depends(get_db)
):

    result = crud.create_user(db, user)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "message": "User Registered Successfully"
    }


# LOGIN

@app.post("/login")
def login(
        user: schemas.UserLogin,
        db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
            user.password,
            db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# EMPLOYEE APIs

@app.post("/employees")
def create_employee(
        employee: schemas.EmployeeCreate,
        db: Session = Depends(get_db)
):
    return crud.create_employee(
        db,
        employee
    )


@app.get("/employees")
def get_employees(
        db: Session = Depends(get_db)
):
    return db.query(models.Employee).all()


@app.get("/employees/{employee_id}")
def get_employee(
        employee_id: int,
        db: Session = Depends(get_db)
):

    emp = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not emp:
        raise HTTPException(
            404,
            "Employee Not Found"
        )

    return emp


@app.put("/employees/{employee_id}")
def update_employee(
        employee_id: int,
        employee: schemas.EmployeeCreate,
        db: Session = Depends(get_db)
):

    emp = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not emp:
        raise HTTPException(
            404,
            "Employee Not Found"
        )

    emp.name = employee.name
    emp.email = employee.email
    emp.department = employee.department

    db.commit()

    return {"message": "Updated Successfully"}


@app.delete("/employees/{employee_id}")
def delete_employee(
        employee_id: int,
        db: Session = Depends(get_db)
):

    emp = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not emp:
        raise HTTPException(
            404,
            "Employee Not Found"
        )

    db.delete(emp)
    db.commit()

    return {"message": "Deleted Successfully"}


# TICKET APIs

@app.post("/tickets")
def create_ticket(
        ticket: schemas.TicketCreate,
        db: Session = Depends(get_db)
):
    return crud.create_ticket(
        db,
        ticket
    )


@app.get("/tickets")
def get_tickets(
        db: Session = Depends(get_db)
):
    return db.query(models.Ticket).all()


@app.get("/tickets/{ticket_id}")
def get_ticket(
        ticket_id: int,
        db: Session = Depends(get_db)
):

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            404,
            "Ticket Not Found"
        )

    return ticket


@app.put("/tickets/{ticket_id}")
def update_ticket(
        ticket_id: int,
        ticket_data: schemas.TicketUpdate,
        db: Session = Depends(get_db)
):

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            404,
            "Ticket Not Found"
        )

    if ticket_data.title:
        ticket.title = ticket_data.title

    if ticket_data.description:
        ticket.description = ticket_data.description

    if ticket_data.priority:
        ticket.priority = ticket_data.priority

    if ticket_data.status:
        ticket.status = ticket_data.status

    db.commit()

    return {"message": "Ticket Updated"}


@app.delete("/tickets/{ticket_id}")
def delete_ticket(
        ticket_id: int,
        db: Session = Depends(get_db)
):

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            404,
            "Ticket Not Found"
        )

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket Deleted"}


# ASSIGN TICKET

@app.post(
    "/tickets/{ticket_id}/assign/{employee_id}"
)
def assign_ticket(
        ticket_id: int,
        employee_id: int,
        db: Session = Depends(get_db)
):

    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id
    ).first()

    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not ticket:
        raise HTTPException(
            404,
            "Ticket Not Found"
        )

    if not employee:
        raise HTTPException(
            404,
            "Employee Not Found"
        )

    ticket.assigned_employee_id = employee_id

    db.commit()

    return {
        "message": "Ticket Assigned"
    }


@app.get(
    "/employees/{employee_id}/tickets"
)
def employee_tickets(
        employee_id: int,
        db: Session = Depends(get_db)
):

    return db.query(models.Ticket).filter(
        models.Ticket.assigned_employee_id
        == employee_id
    ).all()