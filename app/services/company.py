from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.company import CompanyModel, SearchCompanyModel
from schemas.company import Company
from services.utils import get_current_utc_time


def get_companies(db: Session, conds: SearchCompanyModel) -> List[Company]:
    # Default of joinedload is LEFT OUTER JOIN
    query = select(Company)
    
    if conds.name is not None:
        query = query.filter(Company.name.like(f"{conds.name}%"))    
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()


def get_company_by_id(db: Session, id: UUID, /, joined_load = False) -> Company:
    query = select(Company).filter(Company.id == id)
    
    return db.scalars(query).first()
    

def add_new_company(db: Session, data: CompanyModel) -> Company:    

    company = Company(**data.model_dump())
    company.created_at = get_current_utc_time()
    company.updated_at = get_current_utc_time()

    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company
