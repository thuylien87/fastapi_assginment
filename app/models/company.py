from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from schemas.company import CompanyMode

class SearchCompanyModel():
    def __init__(self, name, description, page, size) -> None:
        self.name = name
        self.description = description
        self.page = page
        self.size = size

class CompanyModel(BaseModel):
    name: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)    
    mode: CompanyMode = Field(default=CompanyMode.DRAFT)
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company 1",
                "description": "Description for Company 1",
                "rating": 4,                
                "mode": "D"
            }
        }

class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    rating: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True
