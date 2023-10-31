from pydantic import ValidationError

from main_machine_monitoring.database import orm_class
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import has_inherited_table, Session
from main_machine_monitoring.database import db_setup
from main_machine_monitoring.pydantic_schema.request_schema import Edit, UpdateElement, UpdateWelder
from main_machine_monitoring.router.oauth2 import get_current_user

router = APIRouter(
    prefix="/edit",
    tags=['edit']
)


@router.put("/{type}/{welder_name}")
def update_data(type: str, welder_name: str, element: Edit, db: Session = Depends(db_setup.get_db)):
    if element.voltage is not None and element.current is not None and element.element_description is not None:
        # Update Element table
        element_update_query = db.query(orm_class.Element).filter(orm_class.Element.type == type)
        update_element = element_update_query.first()

        if update_element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Element with type:{type} does not exist")

        # Create a dictionary with only Element attributes
        element_data = {
            "voltage": element.voltage,
            "current": element.current,
            "element_description": element.element_description,
            "range": element.range
        }

        element_update_query.update(element_data, synchronize_session=False)

    if element.I_no is not None and element.Fc_no is not None and element.project is not None:
        # Update Welder table
        welder_update_query = db.query(orm_class.Welder).filter(orm_class.Welder.welder_name == welder_name)
        update_welder = welder_update_query.first()

        if update_welder is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Welder with welder_name:{welder_name} does not exist")

        # Create a dictionary with only Welder attributes
        welder_data = {
            "I_no": element.I_no,
            "Fc_no": element.Fc_no,
            "project": element.project
        }

        welder_update_query.update(welder_data, synchronize_session=False)

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid data provided")

    db.commit()
    return {"message": "Data updated successfully"}


# updating elements
@router.put("/{type}")
def update_post(type: str, element: UpdateElement, db: Session = Depends(db_setup.get_db),
                user_id: int = Depends(get_current_user)):
    print("==============================================")
    print(user_id)
    print("==============================================")
    element_update_query = db.query(orm_class.Element).filter(orm_class.Element.type == type)
    update_element = element_update_query.first()

    # if not found
    if update_element is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"machine with type:{type} does not exsist")

    # if found
    element_update_query.update(element.dict(), synchronize_session=False)
    db.commit()
    return {"updated_element_is ": element_update_query.first()}
