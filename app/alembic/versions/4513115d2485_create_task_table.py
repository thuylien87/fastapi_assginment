"""Create task table

Revision ID: 4513115d2485
Revises: 4ba8cbc3cdea
Create Date: 2024-08-27 16:56:53.661810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas.task import TaskMode


# revision identifiers, used by Alembic.
revision: str = '4513115d2485'
down_revision: str = '4513115d2484'
branch_labels: None
depends_on: None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status', sa.Enum(TaskMode), nullable=False, default=TaskMode.ACTIVE),
        sa.Column('priority', sa.SmallInteger, default=0),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.add_column("tasks", sa.Column("user_id", sa.UUID, nullable=True))
    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_table('tasks')
    op.execute("DROP TYPE taskmode;")