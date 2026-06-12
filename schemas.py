from pydantic import BaseModel, EmailStr
from typing import Optional


# Authentication

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Employee

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True


# Ticket

class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    assigned_employee_id: Optional[int]

    class Config:
        from_attributes = True