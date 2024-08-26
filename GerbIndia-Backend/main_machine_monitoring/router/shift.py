# from main_machine_monitoring.database import orm_class
# from main_machine_monitoring.pydantic_schema.request_schema import ShiftBase
# from fastapi import Depends, APIRouter
# from sqlalchemy.orm import Session
# from main_machine_monitoring.database.db_setup import get_db
#
#
# router = APIRouter(
#     prefix="/shift",
#     tags=['shift']
# )
#
#
# @router.post("/")
# def create_shift(shift_data: ShiftBase, db: Session = Depends(get_db)):
#     new_shift = orm_class.Shift(**shift_data.dict())
#     db.add(new_shift)
#     db.commit()
#     db.refresh(new_shift)
#     return new_shift
#
#
# # get all shifts data
# @router.get("/")
# def test(db: Session = Depends(get_db)):
#     # select * from shifts
#     shifts = db.query(orm_class.Shift).all()
#     return {"Data": shifts}
#
