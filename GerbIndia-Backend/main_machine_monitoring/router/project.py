# from main_machine_monitoring.database import orm_class
# from main_machine_monitoring.pydantic_schema import request_schema
# from fastapi import status, HTTPException, Depends, APIRouter
# from sqlalchemy.orm import Session
# from main_machine_monitoring.database import db_setup
# from datetime import datetime
#
# router = APIRouter(
#     prefix="/project",
#     tags=['project']
# )
#
#
# @router.get("/")
# def test(db: Session = Depends(db_setup.get_db)):
#     # select * from machine
#     Project = db.query(orm_class.Project).all()
#     return {"Data": Project}
#
#
# # CREATING elements
# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_post(project: request_schema.CreateProject, db: Session = Depends(db_setup.get_db)):
#     print("Got new request at:", datetime.now())
#
#     new_project = orm_class.Project(**project.dict())
#
#     db.add(new_project)
#     db.commit()
#     db.refresh(new_project)
#     return new_project
#
#
# @router.put("/{project}")
# def update_post(project: str, project_schema: request_schema.UpdateProject, db: Session = Depends(db_setup.get_db)):
#     project_update_query = db.query(orm_class.Project).filter(orm_class.Project.project == project)
#
#     update_project = project_update_query.first()
#
#     # if not found
#     if update_project is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#
#                             detail=f"welder {project} does not exist")
#     project_update_query.update(project_schema.dict(), synchronize_session=False)
#     db.commit()
#
#     return {"updated"}
#
#
# @router.delete("/{project_name}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(project_name: str, I_no: str, Fc_no: str, db: Session = Depends(db_setup.get_db)):
#     delete_project = db.query(orm_class.Project).filter(
#         (orm_class.Project.project == project_name) &
#         (orm_class.Project.I_no == I_no) &
#         (orm_class.Project.Fc_no == Fc_no)
#     )
#
#     # if not found
#     if delete_project.first() is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Project with name: {project_name}, I_no: {I_no}, and Fc_no: {Fc_no} does not exist"
#         )
#
#     # if found
#     delete_project.delete(synchronize_session=False)
#     db.commit()
#     return {"message": "Project was deleted"}
