from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models import company
from schemas import User
from models.user import UserModel, SearchUserModel
from services import company as CompanyService
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError, InvalidInputError


def get_users(db: Session, conds: SearchUserModel) -> List[User]:    
    query = select(User).filter(User.is_active == True)
    if conds.username is not None:
        query = query.filter(User.username.like(f"{conds.username}%"))
    if conds.company_id is not None:
        query = query.filter(User.company_id == conds.company_id)
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()


def get_user_by_id(db: Session, id: UUID, /) -> User:
    query = select(User).filter(User.id == id)
        
    return db.scalars(query).first()
    

def add_new_user(db: Session, data: UserModel) -> User:
    company = CompanyService.get_company_by_id(db, data.company_id)
        
    if company is None:
        raise InvalidInputError("Invalid company information")

    user = User(**data.model_dump())
    user.created_at = get_current_utc_time()
    user.updated_at = get_current_utc_time()

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def update_user(db: Session, id: UUID, data: UserModel) -> User:
    user = get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()

    if data.company_id != user.company_id:
        company = CompanyService.get_company_by_id(db, data.company_id)
        if company is None:
            raise InvalidInputError("Invalid company information")
    
    user.username = data.username
    user.email = data.email
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.company_id = data.company_id
    
    user.updated_at = get_current_utc_time()
    
    db.commit()
    db.refresh(user)
    
    return user
