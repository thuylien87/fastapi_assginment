"""Create company table

Revision ID: 4ba8cbc3cdea
Revises: 
Create Date: 2024-08-27 16:56:45.802877

"""
from uuid import uuid4
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

from schemas.company import CompanyMode


# revision identifiers, used by Alembic.
revision: str = '4ba8cbc3cdea'
down_revision: str = None
branch_labels: None
depends_on: None


def upgrade() -> None:
    company_table = op.create_table(
        'companies',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.DRAFT),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    
    # Data seed for company
    op.bulk_insert(company_table, [
        {
            "id": uuid4(),
            "name": "Company 1", 
            "description": "Description for Company 1",
            "mode": "PUBLISHED",
            "rating": "5",            
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid4(),
            "name": "Company 2", 
            "description": "Description for Company 2",
            "mode": "PUBLISHED",
            "rating": "3",            
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid4(),
            "name": "Company 3", 
            "description": "Description for Company 3",
            "mode": "PUBLISHED",
            "rating": "5",            
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid4(),
            "name": "Company 4", 
            "description": "Description for Company 4",
            "mode": "DRAFT",
            "rating": "4",            
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "id": uuid4(),
            "name": "Company 5", 
            "description": "Description for Company 5",
            "mode": "PUBLISHED",
            "rating": "5",            
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])


def downgrade() -> None:
    op.drop_table('companies')
    op.execute("DROP TYPE companymode;")
