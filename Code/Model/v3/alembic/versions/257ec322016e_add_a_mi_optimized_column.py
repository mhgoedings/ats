"""Add a mi_optimized column

Revision ID: 257ec322016e
Revises: c1246af47260
Create Date: 2018-11-15 12:59:32.266574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '257ec322016e'
down_revision = 'c1246af47260'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("strategies", sa.Column("mi_optimized", sa.Integer, default=0, nullable=True))


def downgrade():
    op.drop_column("strategies", "mi_optimized")

