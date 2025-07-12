"""add WAITING and REFUSED to status_enum

Revision ID: 6c07e2a8b303
Revises: dd66074107a1
Create Date: 2025-07-12 02:47:02.541220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c07e2a8b303'
down_revision = 'dd66074107a1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE status_enum ADD VALUE IF NOT EXISTS 'WAITING'")
    op.execute("ALTER TYPE status_enum ADD VALUE IF NOT EXISTS 'REFUSED'")
        

def downgrade():
    pass
