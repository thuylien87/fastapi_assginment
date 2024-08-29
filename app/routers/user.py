from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import UserModel
from schemas import User
from models import UserViewModel, SearchUserModel
from services import auth as AuthService
from services import user as UserService
from services.exception import AccessDeniedError, ResourceNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserViewModel])
async def get_users(
    username: str = Query(default=None),
    email: str = Query(default=None),
    first_name: str = Query(default=None),    
    last_name: str = Query(default=None),     
    company_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
    
        if not user.is_admin:
            raise AccessDeniedError()
        
        conds = SearchUserModel(username, email, first_name, last_name, company_id, page, size)    
        return UserService.get_users(db, conds)
    
    
@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(
    request: UserModel, 
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
    ):
        if not user:
            raise AccessDeniedError()

        return UserService.add_new_user(db, request)
    
@router.get("/{user_id}", response_model=UserViewModel)
async def get_user_detail(
    user_id: UUID, 
    db: Session=Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()
        
        user_response = UserService.get_user_by_id(db, user_id)
        
        if user_response is None:
            raise ResourceNotFoundError()

        return user_response


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user(
    user_id: UUID,
    request: UserModel,
    db: Session=Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user:
            raise AccessDeniedError()
        
        return UserService.update_user(db, user_id, request)