from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property

from main_machine_monitoring.database.db_setup import Base
from sqlalchemy.sql.expression import column, null, text
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Float, ForeignKey, func, Date, Numeric, DateTime
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import Time
from main_machine_monitoring.pydantic_schema.request_schema import ShiftOp


class Logs(Base):
    __tablename__ = "vol_cur_logs"

    id = Column(Integer, primary_key=True, nullable=False)
    machine_id = Column(String, nullable=True)
    time = Column(DateTime, nullable=False)
    voltage = Column(Numeric(precision=6, scale=2), nullable=False)
    current = Column(Numeric(precision=6, scale=2), nullable=False)


class Welder(Base):
    __tablename__ = "Welder details"

    id = Column(Integer, primary_key=True, nullable=False)
    welder_name = Column(String, nullable=True)
    welder_number = Column(Integer, nullable=False)
    date_of_joining = Column(Date, nullable=False)
    welder_qualification = Column(String, nullable=False)
    qualified_thickness = Column(Integer, nullable=False)
    I_no = Column(String, nullable=False)
    Fc_no = Column(String, nullable=False)
    project = Column(String, nullable=False)

    # Adding the one-to-many relationship
    shift_op = relationship("ShiftOp", back_populates="welder", lazy="dynamic")


class Element(Base):
    __tablename__ = "Element Type"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    range = Column(String, nullable=True)
    current = Column(String, nullable=False)
    voltage = Column(String, nullable=False)
    element_description = Column(String, nullable=True)

    # Adding the one-to-many relationship
    shift_op = relationship("ShiftOp", back_populates="element", lazy="dynamic")


class Machine(Base):
    __tablename__ = "Machine"

    id = Column(Integer, primary_key=True, nullable=False)
    machine_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    maker = Column(String, nullable=False)
    capacity_in_amp = Column(Integer, nullable=False)
    date_of_purchase = Column(String, nullable=False)

    # Adding the one-to-many relationship with Live and LiveRecent
    live_data = relationship("Live", back_populates="machine", lazy="dynamic")
    live_recent_data = relationship("LiveRecent", back_populates="machine", lazy="dynamic")
    shift_op = relationship("ShiftOp", back_populates="machine", lazy="dynamic")


class Shift(Base):
    __tablename__ = "shift"

    id = Column(Integer, primary_key=True, nullable=False)
    shift = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Adding a relationship to ShiftOp
    shift_ops = relationship("ShiftOp", back_populates="shift")


class ShiftOp(Base):
    __tablename__ = "operator_shift"

    id = Column(Integer, primary_key=True, nullable=False)
    # operator_id = Column(String, nullable=False)
    # Type_id = Column(String, nullable=False)
    # machine_id = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    duration = Column(Float, nullable=False)  # Add duration as a regular column

    # Adding the foreign key to the Machine table
    machine_id = Column(Integer, ForeignKey('Machine.id'), nullable=False)
    machine = relationship("Machine", back_populates="shift_op")

    # Adding the foreign key to the Element table table
    element_id = Column(Integer, ForeignKey('Element Type.id'), nullable=False)
    element = relationship("Element", back_populates="shift_op")

    # Adding the foreign key to the Element table table
    operator_id = Column(Integer, ForeignKey('Welder details.id'), nullable=False)
    welder = relationship("Welder", back_populates="shift_op")

    # Adding the foreign key to the Shift table
    shift_id = Column(Integer, ForeignKey('shift.id'), nullable=False)  # Foreign key to the 'id' column of 'Shift'
    shift = relationship("Shift", back_populates="shift_ops")


class Live(Base):
    __tablename__ = "live_data"

    id = Column(Integer, primary_key=True, nullable=False)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Adding the foreign key to the Machine table
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="live_data")


class LiveRecent(Base):
    __tablename__ = "Live_recent"

    id = Column(Integer, primary_key=True, nullable=False)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Adding the foreign key to the Machine table
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="live_recent_data")


class Test(Base):
    __tablename__ = "data stimulation"

    id = Column(Integer, primary_key=True, nullable=False)
    current = Column(Integer, nullable=False)
    state = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))


class User(Base):
    __tablename__ = "Admin login"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))


class SpareMachine(Base):
    __tablename__ = "spare_Machine"

    id = Column(Integer, primary_key=True, nullable=False)
    machine_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    maker = Column(String, nullable=False)
    capacity_in_amp = Column(Integer, nullable=False)
    date_of_purchase = Column(String, nullable=False)


