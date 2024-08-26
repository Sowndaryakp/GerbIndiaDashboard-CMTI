from main_machine_monitoring.database.db_setup import Base
from sqlalchemy.sql.expression import column, null, text
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Float, ForeignKey, func, Date, Numeric, DateTime, \
    Index
from sqlalchemy.orm import relationship, column_property


class Plate(Base):
    __tablename__ = "plate"

    id = Column(Integer, primary_key=True, nullable=False)
    plate_thickness = Column(String, nullable=True)
    plate_description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Adding the foreign key to the Element table table
    element_id = Column(Integer, ForeignKey('Element Type.id'), nullable=False)
    element_type = relationship("Element", back_populates="plate")
    shift_op = relationship("ShiftOp", back_populates="plate", lazy="dynamic")


class Remarks(Base):
    __tablename__ = "remarks"

    id = Column(Integer, primary_key=True, nullable=False)
    Remarks = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Adding the foreign key to the Element table table
    operator_id = Column(Integer, ForeignKey('Welder details.id'), nullable=False)
    welder_remarks = relationship("Welder", back_populates="remarks")
    shift_op = relationship("ShiftOp", back_populates="remarks", lazy="dynamic")


class ShiftOp(Base):
    __tablename__ = "operator_shift"

    id = Column(Integer, primary_key=True, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    duration = Column(Float, nullable=False)  # Add duration as a regular column
    I_no = Column(String, nullable=True)
    Fc_no = Column(String, nullable=True)
    project = Column(String, nullable=True)

    # Adding the foreign key to the Machine table
    machine_id = Column(Integer, ForeignKey('Machine.id'), nullable=False)
    machine = relationship("Machine", back_populates="shift_op")

    # Adding the foreign key to the Element table table
    element_id = Column(Integer, ForeignKey('Element Type.id'), nullable=False)
    element = relationship("Element", back_populates="shift_op")

    # Adding the foreign key to the Element table table
    operator_id = Column(Integer, ForeignKey('Welder details.id'), nullable=False)
    welder = relationship("Welder", back_populates="shift_op")

    # Adding the foreign key to the Element table table
    plate_id = Column(Integer, ForeignKey('plate.id'), nullable=False)
    plate = relationship("Plate", back_populates="shift_op")

    # Adding the foreign key to the Element table table
    remarks_id = Column(Integer, ForeignKey('remarks.id'), nullable=False)
    remarks = relationship("Remarks", back_populates="shift_op")


class Welder(Base):
    __tablename__ = "Welder details"

    id = Column(Integer, primary_key=True, nullable=False)
    welder_name = Column(String, nullable=False)
    welder_number = Column(Integer, nullable=False, unique=True)
    date_of_joining = Column(Date, nullable=False)
    welder_qualification = Column(String, nullable=False)
    qualified_thickness = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    # Adding the one-to-many relationship
    shift_op = relationship("ShiftOp", back_populates="welder", lazy="dynamic")
    remarks = relationship("Remarks", back_populates="welder_remarks", lazy="dynamic")


class Element(Base):
    __tablename__ = "Element Type"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False, unique=True)
    range = Column(String, nullable=True)
    standard_current = Column(String, nullable=False)
    standard_voltage = Column(String, nullable=False)
    element_description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    shift_op = relationship("ShiftOp", back_populates="element", lazy="dynamic")
    type_sd = relationship("StandardData", back_populates="type", lazy="dynamic")
    plate = relationship("Plate", back_populates="element_type", lazy="dynamic")


class Logs(Base):
    __tablename__ = "vol_cur_logs"

    id = Column(Integer, primary_key=True, nullable=False)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="logs_data")


class StandardData(Base):
    __tablename__ = "std_cur_vol"

    id = Column(Integer, primary_key=True, nullable=False)
    low_std_curr = Column(Integer, nullable=False)
    high_std_curr = Column(Integer, nullable=False)
    low_std_vol = Column(Integer, nullable=True)
    high_std_vol = Column(Integer, nullable=True)

    type_id = Column(String, ForeignKey('Element Type.type'), nullable=False)
    type = relationship("Element", back_populates="type_sd")


class Live(Base):
    __tablename__ = "live_data"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, primary_key=True, server_default=text('now()'))
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False, primary_key=True)

    machine = relationship("Machine", back_populates="live_data")

class Graph(Base):
    __tablename__ = "graph_data"

    id = Column(Integer, primary_key=True, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    state = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    color = Column(String, nullable=False)  # Add the color column here

    # Assuming you have a machine_id relationship
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="graph_data")


class State(Base):
    __tablename__ = "check_state"

    id = Column(Integer, primary_key=True, nullable=False)
    start_range_current = Column(Float, nullable=False)
    end_range_current = Column(Float, nullable=False)
    start_range_voltage = Column(Float, nullable=False)
    end_range_voltage = Column(Float, nullable=False)
    state = Column(String, nullable=False)
    color = Column(String, nullable=False)


class LiveRecent(Base):
    __tablename__ = "Live_recent"

    id = Column(Integer, primary_key=True, nullable=False ,autoincrement=True)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    state = Column(Boolean, nullable=True)
    machine_state = Column(Boolean, nullable=True)

    # Adding the foreign key to the Machine table
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="live_recent_data")


class On(Base):
    __tablename__ = "ON_data"

    id = Column(Integer, primary_key=True, nullable=False)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Adding the foreign key to the Machine table
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="ON_data")


class Production(Base):
    __tablename__ = "Production_data"

    id = Column(Integer, primary_key=True, nullable=False)
    current = Column(Float, nullable=False)
    voltage = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Adding the foreign key to the Machine table
    machine_id = Column(String, ForeignKey('Machine.machine_id'), nullable=False)
    machine = relationship("Machine", back_populates="production_data")


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
    logs_data = relationship("Logs", back_populates="machine", lazy="dynamic")
    ON_data = relationship("On", back_populates="machine", lazy="dynamic")
    production_data = relationship("Production", back_populates="machine", lazy="dynamic")
    graph_data = relationship("Graph", back_populates="machine", lazy="dynamic")


class User(Base):
    __tablename__ = "Admin login"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Inst(Base):
    __tablename__ = "instruction"

    id = Column(Integer, primary_key=True, nullable=False)
    instruction = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

