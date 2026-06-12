from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(30), unique=True, index=True)
    password = Column(String(40))
    role = Column(String(25))


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(30), unique=True)
    department = Column(String(50))


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    priority = Column(String(50))
    status = Column(String(70), default="Open")

    assigned_employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True
    )

    employee = relationship("Employee")