from sqlalchemy.exc import IntegrityError

from main_machine_monitoring.database import orm_class
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main_machine_monitoring.database import db_setup
from datetime import datetime

from urllib.parse import unquote

router = APIRouter(
    prefix="/elements",
    tags=['elements']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(element: request_schema.CreateElement, db: Session = Depends(db_setup.get_db)):
    print("Got new request at:", datetime.now())

    existing_element = db.query(orm_class.Element).filter_by(type=element.type).first()

    if existing_element:
        raise HTTPException(status_code=400, detail=f"Element with type '{element.type}' already exists")

    new_element = orm_class.Element(**element.dict())
    print("----------------------------------------------------------------------")
    print(new_element)
    # Extracting standard_current and standard_voltage values
    standard_current_values = element.standard_current.split("-")
    standard_voltage_values = element.standard_voltage.split("-")

    # Validating the format of standard_current and standard_voltage values
    if len(standard_current_values) != 2 or len(standard_voltage_values) != 2:
        raise HTTPException(status_code=400, detail="Invalid format for standard_current or standard_voltage")

    try:
        # Creating the Element instance
        db.add(new_element)
        db.commit()
        db.refresh(new_element)

        # Creating corresponding entry in StandardData table
        new_standard_data = orm_class.StandardData(
            low_std_curr=int(standard_current_values[0]),
            high_std_curr=int(standard_current_values[1]),
            low_std_vol=int(standard_voltage_values[0]),
            high_std_vol=int(standard_voltage_values[1]),
            type_id=new_element.type  # Assuming 'type' in Element corresponds to 'type_id' in StandardData
        )

        db.add(new_standard_data)
        db.commit()
        db.refresh(new_standard_data)

        return new_element

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create element: {str(e)}")


@router.get("/type", response_model=request_schema.ReturnType)
def root(type: str = Depends(unquote), db: Session = Depends(db_setup.get_db)):
    print(f"Searching for type: {type}")

    element = db.query(orm_class.Element).filter(orm_class.Element.type == type).first()

    # If element is not found
    if not element:
        raise HTTPException(status_code=404, detail=f"The element with type: {type} was not found")

    # Check if element is active
    if not element.is_active:
        raise HTTPException(status_code=404, detail=f"The element with type: {type} does not exist or is inactive")

    return element


@router.delete("/type", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(type: str = Depends(unquote), db: Session = Depends(db_setup.get_db)):
    element = db.query(orm_class.Element).filter(orm_class.Element.type == type).first()

    if element is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Element with type: {type} does not exist")

    # Update is_active to False instead of deleting the element
    element.is_active = False
    db.commit()

    return {"message": f"Element '{type}' is now inactive"}


@router.put("/type")
def update_post(element: request_schema.UpdateElement, db: Session = Depends(get_db),type: str = Depends(unquote)):
    element_update_query = db.query(orm_class.Element).filter(orm_class.Element.type == type)
    update_element = element_update_query.first()

    # if not found
    if update_element is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Machine with model:{type} does not exist")

    try:
        # Update the Element details
        element_update_query.update(element.dict(), synchronize_session=False)
        db.commit()

        # Update or create associated StandardData
        standard_data = db.query(orm_class.StandardData).filter_by(type_id=update_element.type).first()
        if standard_data:
            # Update existing StandardData entry
            standard_data.low_std_curr = int(element.standard_current.split("-")[0])
            standard_data.high_std_curr = int(element.standard_current.split("-")[1])
            standard_data.low_std_vol = int(element.standard_voltage.split("-")[0])
            standard_data.high_std_vol = int(element.standard_voltage.split("-")[1])
        else:
            # Create a new StandardData entry
            new_standard_data = orm_class.StandardData(
                low_std_curr=int(element.standard_current.split("-")[0]),
                high_std_curr=int(element.standard_current.split("-")[1]),
                low_std_vol=int(element.standard_voltage.split("-")[0]),
                high_std_vol=int(element.standard_voltage.split("-")[1]),
                type_id=update_element.type  # Assuming 'type' in Element corresponds to 'type_id' in StandardData
            )
            db.add(new_standard_data)

        db.commit()
        return {"updated_machine_is ": element_update_query.first()}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update element: {str(e)}")
