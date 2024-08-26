from pydantic import BaseModel, config, EmailStr, validator
from datetime import datetime, date, time
from typing import Optional, List, Dict
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
    standard_current: str
    standard_voltage: str


class CreateElement(ElementBase):
    pass


class UpdateElement(BaseModel):
    range: Optional[str] = None
    standard_current: str
    standard_voltage: str
    element_description: str


class ReturnType(BaseModel):
    type: str
    range: Optional[str] = None
    standard_current: str
    standard_voltage: str
    element_description: Optional[str] = None

    class config:
        orm_mode = True


#
# class ReType(BaseModel):
#     type: str
#     range: Optional[str] = None
#     standard_current: str
#     standard_voltage: str
#     element_description: Optional[str] = None
#
#     class config:
#         orm_mode = True


# WELDER
class WelderBase(BaseModel):
    welder_name: str
    welder_number: int
    date_of_joining: date
    welder_qualification: str
    qualified_thickness: Optional[int] = None


class GetWelder(BaseModel):
    welder_name: str
    welder_number: int
    date_of_joining: date
    welder_qualification: str
    qualified_thickness: Optional[int] = None


# class ReturnWelder(BaseModel):
#     I_no: str
#     Fc_no: str
#     project: str
#
#     class config:
#         orm_mode = True


class CreateWelder(WelderBase):
    pass


class LiveBase(BaseModel):
    current: float
    voltage: float
    created_at: datetime


# EDIT
class Edit(BaseModel):
    element_description: str
    range: str
    I_no: str
    Fc_no: str
    project: str
    remarks: str
    plate_thickness: str
    plate_description: str

    class config:
        orm_mode = True


class UpdateWelder(BaseModel):
    welder_name: str
    date_of_joining: date
    welder_qualification: str
    qualified_thickness: Optional[int] = None


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
# class ShiftBase(BaseModel):
#     shift: str
#     start_time: time
#     end_time: time
#     I_no: str
#     Fc_no: str
#     project: str
#

class ShiftOpCreate(BaseModel):
    operator_name: str
    element_type: str
    machine_name: str
    start_time: int
    end_time: int
    I_no: str
    Fc_no: str
    project: str
    plate_thickness: str
    plate_description: str
    remarks: str


class ShiftOpGet(BaseModel):
    machine_name: str
    element_type: str
    operator_name: str
    start_time: datetime
    end_time: datetime
    I_no: str
    Fc_no: str
    project: str
    plate_thickness: str
    plate_description: str
    remarks: str


# Pydantic models for request and response
class ShiftOpGetnew(BaseModel):
    machine_id: str
    element_type: str
    operator_name: str
    start_time: datetime
    end_time: datetime
    I_no: Optional[str]
    Fc_no: Optional[str]
    project: Optional[str]
    plate_thickness: Optional[str]
    plate_description: Optional[str]
    remarks: Optional[str]

class ShiftOpDisplay(BaseModel):
    machine_id: str
    type: str
    welder_name: str
    start_time: datetime
    end_time: datetime
    I_no: str
    Fc_no: str
    project: str
    standard_current: str
    standard_voltage: str
    average_current: Optional[float] = None
    average_voltage: Optional[float] = None
    min_current: Optional[float] = None
    max_current: Optional[float] = None
    min_voltage: Optional[float] = None
    max_voltage: Optional[float] = None
    range: Optional[str] = None  # Nullable field
    plate_thickness: Optional[str] = None  # Nullable field
    plate_description: Optional[str] = None  # Nullable field


class ShiftOpUpdate(BaseModel):
    element_type: str
    start_time: int
    end_time: int
    I_no: str
    Fc_no: str
    project: str


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


class VoltageData(BaseModel):
    machine: str
    voltage: float


# GRAPH

class Datapoint(BaseModel):
    name: str
    value: List[int]
    itemStyle: Dict


class GraphDataResponse(BaseModel):
    minimumTimestamp: int
    dataPoints: List[Datapoint]


# REPORT
class ReportData(BaseModel):
    machine_id: str
    avg_current: float
    avg_voltage: float


# LOGS
class LogsData(BaseModel):
    low_std_curr: int
    high_std_curr: int
    low_std_vol: int
    high_std_vol: int


class ProductionGraphData(BaseModel):
    machine_id: str
    state: str
    duration: float
    start_time: datetime
    end_time: datetime


class LiveRecentResponse(BaseModel):
    id: int
    current: float
    voltage: float
    created_at: datetime  # You might want to adjust the type of the created_at field based on your needs
    state: bool
    machine_id: str
    machine_state: bool


# REMARKS
class RemarksBase(BaseModel):
    remarks: str
    operator: str


class CreateRemark(RemarksBase):
    pass


class LiveData(BaseModel):
    id: int
    current: float
    voltage: float
    created_at: datetime
    machine_id: str

    class Config:
        orm_mode = True

class InstructionData(BaseModel):
    id: int
    instruction: str

    class Config:
        orm_mode = True

class InstructionCreate(BaseModel):
    instruction: str


class InstructionUpdate(BaseModel):
    instruction: str