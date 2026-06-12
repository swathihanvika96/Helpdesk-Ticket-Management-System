from sqlalchemy.orm import Session
import models
import schemas
from auth import hash_password


# Register User

def create_user(
        db: Session,
        user: schemas.UserRegister
):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if db_user:
        return None

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Employee

def create_employee(
        db: Session,
        employee: schemas.EmployeeCreate
):

    emp = models.Employee(**employee.dict())

    db.add(emp)
    db.commit()
    db.refresh(emp)

    return emp


# Ticket

def create_ticket(
        db: Session,
        ticket: schemas.TicketCreate
):

    new_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status="Open"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket