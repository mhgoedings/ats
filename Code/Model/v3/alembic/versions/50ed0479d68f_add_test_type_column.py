"""Add test_type column

Revision ID: 50ed0479d68f
Revises: 4178d4e83db9
Create Date: 2018-10-21 09:34:46.463130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50ed0479d68f'
down_revision = '4178d4e83db9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("oos_tests", sa.Column("test_type", sa.String(length=12), nullable=True))


def downgrade():
    op.drop_column("oos_tests", "test_type")
