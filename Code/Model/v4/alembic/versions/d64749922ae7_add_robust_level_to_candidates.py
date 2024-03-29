""" add robust_level to candidates

Revision ID: d64749922ae7
Revises: c8e9704f66f4
Create Date: 2019-01-20 11:32:33.822189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64749922ae7'
down_revision = 'c8e9704f66f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidates', sa.Column('robust_level', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('candidates', 'robust_level')
    # ### end Alembic commands ###
