from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from database import get_db_context
from models.company import CompanyModel, CompanyViewModel, SearchCompanyModel
from services import company as CompanyService
from services import auth as AuthService
from services.exception import *
from schemas import User

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[CompanyViewModel])
async def get_all_companies(
    name: str = Query(default=None),
    description: str = Query(default=None),    
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),    
    ):
        conds = SearchCompanyModel(name, description, page, size)
        return CompanyService.get_companies(db, conds)