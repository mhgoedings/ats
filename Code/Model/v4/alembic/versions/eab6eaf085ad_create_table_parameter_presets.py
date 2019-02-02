"""create table parameter_presets

Revision ID: eab6eaf085ad
Revises: ccd19a55a946
Create Date: 2019-01-01 18:45:07.243043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eab6eaf085ad'
down_revision = 'ccd19a55a946'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parameter_presets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('param', sa.String(length=32), nullable=True),
    sa.Column('input_type', sa.String(length=32), nullable=True),
    sa.Column('value', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parameter_presets')
    # ### end Alembic commands ###
