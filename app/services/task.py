from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from services import utils
from services import user as UserService
from models.task import SearchTaskModel, TaskMode, TaskModel
from schemas.task import Task
from services.exception import InvalidInputError, ResourceNotFoundError


def get_tasks(db: Session, conds: SearchTaskModel) -> List[Task]:    
    query = select(Task)    
    if conds.user_id is not None:
        query = query.filter(Task.user_id == conds.user_id)    
    
    return db.scalars(query).all()

def get_task_by_id(db: Session, task_id: UUID) -> Task:
    return db.scalars(select(Task).filter(Task.id == task_id)).first()

def add_new_task(db: Session, data: TaskModel) -> Task:
    user = UserService.get_user_by_id(db, data.user_id)
        
    if user is None:
        raise InvalidInputError("Invalid user information")
    
    task = Task(**data.model_dump())

    task.created_at = utils.get_current_utc_time()
    task.updated_at = utils.get_current_utc_time()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def update_task(db: Session, id: UUID, data: TaskModel) -> Task:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()
    
    user = UserService.get_user_by_id(db, data.user_id)
        
    if user is None:
        raise InvalidInputError("Invalid user information")
    
    task.summary = data.summary
    task.description = data.description
    task.priority = data.priority
    task.user_id = data.user_id
    task.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(task)

    return task

def delete_task(db: Session, id: UUID) -> None:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()
    
    db.delete(task)
    db.commit()
