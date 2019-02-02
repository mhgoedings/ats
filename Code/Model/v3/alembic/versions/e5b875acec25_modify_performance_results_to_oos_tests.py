"""modify performance results to oos_tests

Revision ID: e5b875acec25
Revises: 54bcf463373f
Create Date: 2018-11-16 11:45:34.766662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5b875acec25'
down_revision = '54bcf463373f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oos_tests', sa.Column('drawdown_max', sa.Numeric(precision=12, scale=2), nullable=True))
    op.drop_column('oos_tests', 'max_dd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oos_tests', sa.Column('max_dd', sa.NUMERIC(precision=8, scale=2), autoincrement=False, nullable=True))
    op.drop_column('oos_tests', 'drawdown_max')
    # ### end Alembic commands ###