from typing import List

from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.database.orm_class import Inst
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from main_machine_monitoring.pydantic_schema.request_schema import InstructionCreate, InstructionData, InstructionUpdate

router = APIRouter(
    prefix="/instruction",
    tags=['instruction']
)


@router.post("/post_instructions/", response_model=InstructionCreate)
def create_instruction(instruction: InstructionCreate, db: Session = Depends(get_db)):
    db_instruction = Inst(instruction=instruction.instruction)
    db.add(db_instruction)
    try:
        db.commit()
        db.refresh(db_instruction)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return instruction

@router.get("/get_instructions/", response_model=List[InstructionData])
def read_instructions(db: Session = Depends(get_db)):
    instructions = db.query(Inst).all()
    return instructions


@router.put("/put_instructions/instruction_id", response_model=InstructionData)
def update_instruction(instruction_id: int, updated_instruction: InstructionUpdate, db: Session = Depends(get_db)):
    db_instruction = db.query(Inst).filter(Inst.id == instruction_id).first()
    if db_instruction is None:
        raise HTTPException(status_code=404, detail="Instruction not found")

    db_instruction.instruction = updated_instruction.instruction
    try:
        db.commit()
        db.refresh(db_instruction)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return db_instruction


@router.delete("/delete_instructions/instruction_id", response_model=InstructionData)
def delete_instruction(instruction_id: int, db: Session = Depends(get_db)):
    db_instruction = db.query(Inst).filter(Inst.id == instruction_id).first()
    if db_instruction is None:
        raise HTTPException(status_code=404, detail="Instruction not found")

    db.delete(db_instruction)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return db_instruction