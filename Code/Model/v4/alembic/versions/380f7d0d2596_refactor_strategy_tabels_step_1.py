"""refactor strategy tabels, step 1

Revision ID: 380f7d0d2596
Revises: a85cba9861e4
Create Date: 2019-02-01 22:56:30.529029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '380f7d0d2596'
down_revision = 'a85cba9861e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('strategy_settings', 'status')
    op.drop_column('strategy_settings', 'end_dt')
    op.drop_column('strategy_settings', 'start_dt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('strategy_settings', sa.Column('start_dt', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('strategy_settings', sa.Column('end_dt', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('strategy_settings', sa.Column('status', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
