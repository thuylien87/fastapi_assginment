from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SearchUserModel():
    def __init__(self, username, email, first_name, last_name, company_id, page, size) -> None:
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company_id = company_id
        self.page = page
        self.size = size
        
class UserModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    company_id: UUID
    password: Optional[str]    

class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    company_id: UUID | None = None
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
    created_at: datetime | None = None
    update_at: datetime | None = None
