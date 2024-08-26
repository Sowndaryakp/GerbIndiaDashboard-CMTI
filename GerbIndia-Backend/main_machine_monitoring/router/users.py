from main_machine_monitoring.database import orm_class
from main_machine_monitoring.pydantic_schema import request_schema
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from main_machine_monitoring.database.db_setup import get_db
from main_machine_monitoring.router import utils

router = APIRouter(
    prefix="/users",
    tags=['users']
)


# CRUD operations for users

# creating user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=request_schema.UserOut)
def create_user(user: request_schema.CreateUser, db: Session = Depends(get_db)):
    # hash the password -user.password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = orm_class.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response_user = {
        "id": new_user.id,
        "email": new_user.email,
        "password": new_user.password,
        "created_at": new_user.created_at,
    }

    return response_user


# retrieving user

@router.get("/{id}", response_model=request_schema.UserOut)
def root(id: int, db: Session = Depends(get_db)):
    user = db.query(orm_class.User).filter(orm_class.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with id:{id} not found")

    # Convert the user object to a dictionary
    user_dict = user.__dict__

    # Removing internal SQLAlchemy-related attributes
    user_dict.pop("_sa_instance_state", None)

    # Return the user_dict
    return user_dict

    # return user