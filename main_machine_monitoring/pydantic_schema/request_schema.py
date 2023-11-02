from pydantic import BaseModel, config, EmailStr, validator
from datetime import datetime, date, time
from typing import Optional
from pydantic_settings import BaseSettings


# pydantic models
# MACHINES
class MachineBase(BaseModel):
    machine_id: str
    name: str
    model: str
    maker: str
    capacity_in_amp: int
    date_of_purchase: str


class CreateMachine(MachineBase):
    pass


class SpareMachine(MachineBase):
    pass


class UpdateMachine(MachineBase):
    pass


# ELEMENTS
class ElementBase(BaseModel):
    type: str
    range: Optional[str] = None
    current: str
    voltage: str
    element_description: Optional[str] = None


class CreateElement(ElementBase):
    pass


class UpdateElement(BaseModel):
    range: Optional[str] = None
    current: str
    voltage: str
    element_description: Optional[str] = None


# class ElementInfoSimple(BaseModel):
#     type:str
#     upper_current: int
#     lower_current: int
#     upper_voltage: int
#     lower_voltage: int

class ReturnType(BaseModel):
    type: str
    range: Optional[str] = None
    current: str
    voltage: str

    class config:
        orm_mode = True


# WELDER
class WelderBase(BaseModel):
    welder_name: str
    welder_number: int
    date_of_joining: date
    welder_qualification: str
    qualified_thickness: int
    I_no: str
    Fc_no: str
    project: str


class ReturnWelder(BaseModel):
    I_no: str
    Fc_no: str
    project: str

    class config:
        orm_mode = True


class CreateWelder(WelderBase):
    pass


class LiveBase(BaseModel):
    current: float
    voltage: float
    created_at: datetime


class Edit(BaseModel):
    current: str
    voltage: str
    element_description: str
    range: str
    I_no: str
    Fc_no: str
    project: str

    class config:
        orm_mode = True


class UpdateWelder(BaseModel):
    I_no: str
    Fc_no: str
    project: str

    class config:
        orm_mode = True


# LOGIN
class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class TestStimulation:
    current: int
    state: str
    created_at: datetime


# SHIFT
class ShiftBase(BaseModel):
    shift: str
    start_time: time
    end_time: time


class ShiftOpCreate(BaseModel):
    operator_name: str
    element_type: str
    machine_name: str
    start_time: int
    end_time: int


class ShiftOpGet(BaseModel):
    machine_name: str
    element_type: str
    operator_name: str
    start_time: datetime
    end_time: datetime
    shift: str


class ShiftOpUpdate(BaseModel):
    element_type: str
    start_time: int
    end_time: int


class ShiftOp(ShiftOpCreate):
    id: int
    duration: float

    def __init__(self, **data):
        # Calculate the duration based on the provided start_time and end_time
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        if start_time and end_time:
            duration = (end_time - start_time).total_seconds() / 3600.0  # Calculate duration in hours
        else:
            duration = None

        # Call the superclass constructor with the calculated duration
        super().__init__(**data, duration=duration)

# class CreateShift(ShiftOp):
#     pass


class IpPhase(BaseSettings):
    ip_address: str = "127.0.0.1"
    #
    # class Config:
    #     env_file = ".env"  # Optional: Load environment variables from a file


settings = IpPhase()


class SchedulingBase(BaseModel):
    machine_name: str
    machine_id: str
    operator: str
    part_no: str
    project_id: str
    shift: str


# def __init__(self, **data):
    #     # Calculate the duration based on the provided start_time and end_time
    #     start_time = data.get("start_time")
    #     end_time = data.get("end_time")
    #     if start_time and end_time:
    #         duration = (end_time - start_time).total_seconds() / 3600.0  # Calculate duration in hours
    #     else:
    #         duration = None
    #
    #     # Call the superclass constructor with the calculated duration
    #     super().__init__(**data, duration=duration)
