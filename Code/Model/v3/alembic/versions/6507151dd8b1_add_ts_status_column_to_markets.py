"""add TS status column to markets

Revision ID: 6507151dd8b1
Revises: 8821a056315d
Create Date: 2018-10-26 20:57:53.869756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6507151dd8b1'
down_revision = '8821a056315d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("markets", sa.Column("ts_status", sa.String(12), nullable=True))


def downgrade():
    op.drop_column("markets", "ts_status")
