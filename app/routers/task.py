from uuid import UUID
from starlette import status
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db_context, get_db_context
from models.task import SearchTaskModel, TaskModel, TaskViewModel
from schemas.company import Company
from schemas.user import User
from services.exception import AccessDeniedError, ResourceNotFoundError
from services import task as TaskService
from services import auth as AuthService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# @router.get("", response_model=list[TaskViewModel])
# async def get_all_tasks(async_db: AsyncSession = Depends(get_async_db_context)):
#     return await TaskService.get_tasks(async_db)
@router.get("", response_model=list[TaskViewModel])
async def get_all_tasks(
        user_id: UUID = Query(default=None),
        db: Session = Depends(get_db_context), 
        user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()   
    
        conds = SearchTaskModel(user_id)
        return TaskService.get_tasks(db, conds)


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def get_task_by_id(
    task_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()
        
        task = TaskService.get_task_by_id(db, task_id)

        if task is None:
            raise ResourceNotFoundError()

        return task


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()
        
        return TaskService.add_new_task(db, request)


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_Task(
    task_id: UUID,
    request: TaskModel,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()
    
        return TaskService.update_task(db, task_id, request)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()
   
        TaskService.delete_task(db, task_id)
