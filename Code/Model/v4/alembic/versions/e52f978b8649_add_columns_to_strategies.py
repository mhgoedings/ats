"""add columns to strategies

Revision ID: e52f978b8649
Revises: 9e57469bda5d
Create Date: 2019-01-21 12:24:05.301975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e52f978b8649'
down_revision = '9e57469bda5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('strategies', sa.Column('comm_entry_dol', sa.Numeric(precision=8, scale=4), nullable=True))
    op.add_column('strategies', sa.Column('comm_exit_dol', sa.Numeric(precision=8, scale=4), nullable=True))
    op.add_column('strategies', sa.Column('day_swing', sa.Integer(), nullable=True))
    op.add_column('strategies', sa.Column('fitness_function', sa.String(length=12), nullable=True))
    op.add_column('strategies', sa.Column('lsb', sa.Integer(), nullable=True))
    op.add_column('strategies', sa.Column('max_days_back', sa.Integer(), nullable=True))
    op.add_column('strategies', sa.Column('oos_end_dt', sa.Date(), nullable=True))
    op.add_column('strategies', sa.Column('oos_param_history', sa.Text(), nullable=True))
    op.add_column('strategies', sa.Column('oos_start_dt', sa.Date(), nullable=True))
    op.add_column('strategies', sa.Column('slippage_entry_dol', sa.Numeric(precision=8, scale=4), nullable=True))
    op.add_column('strategies', sa.Column('slippage_exit_dol', sa.Numeric(precision=8, scale=4), nullable=True))
    op.add_column('strategies', sa.Column('strat_type', sa.String(length=12), nullable=True))
    op.add_column('strategies', sa.Column('strategy_oos_file', sa.String(length=250), nullable=True))
    op.add_column('strategies', sa.Column('trades_per_day', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('strategies', 'trades_per_day')
    op.drop_column('strategies', 'strategy_oos_file')
    op.drop_column('strategies', 'strat_type')
    op.drop_column('strategies', 'slippage_exit_dol')
    op.drop_column('strategies', 'slippage_entry_dol')
    op.drop_column('strategies', 'oos_start_dt')
    op.drop_column('strategies', 'oos_param_history')
    op.drop_column('strategies', 'oos_end_dt')
    op.drop_column('strategies', 'max_days_back')
    op.drop_column('strategies', 'lsb')
    op.drop_column('strategies', 'fitness_function')
    op.drop_column('strategies', 'day_swing')
    op.drop_column('strategies', 'comm_exit_dol')
    op.drop_column('strategies', 'comm_entry_dol')
    # ### end Alembic commands ###
