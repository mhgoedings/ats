"""add candidate_config and candidate_param

Revision ID: fe75fddbbbb2
Revises: ecf9bf739e6e
Create Date: 2018-12-28 00:04:56.535053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe75fddbbbb2'
down_revision = 'ecf9bf739e6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate_configs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test_id', sa.Integer(), nullable=True),
    sa.Column('proto_id', sa.Integer(), nullable=True),
    sa.Column('sec_id', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.Column('template_version', sa.String(length=12), nullable=False),
    sa.Column('symbol', sa.String(length=12), nullable=True),
    sa.Column('chart_series', sa.String(length=255), nullable=True),
    sa.Column('fitness_function', sa.String(length=12), nullable=True),
    sa.Column('max_bars_back', sa.Integer(), nullable=True),
    sa.Column('trades_per_day', sa.Integer(), nullable=True),
    sa.Column('day_swing', sa.Integer(), nullable=True),
    sa.Column('start_dt', sa.Date(), nullable=True),
    sa.Column('end_dt', sa.Date(), nullable=True),
    sa.Column('bt_start_dt', sa.Date(), nullable=True),
    sa.Column('bt_end_dt', sa.Date(), nullable=True),
    sa.Column('strategy_file', sa.String(length=250), nullable=False),
    sa.Column('strategy_name', sa.String(length=250), nullable=False),
    sa.Column('status', sa.String(length=12), nullable=True),
    sa.Column('status_state', sa.String(length=12), nullable=True),
    sa.Column('start_run', sa.DateTime(), nullable=True),
    sa.Column('end_run', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['proto_id'], ['proto_configs.id'], ),
    sa.ForeignKeyConstraint(['sec_id'], ['markets.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('candidate_parameters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('input_type', sa.String(length=32), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=False),
    sa.Column('data_type', sa.String(length=8), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidate_parameters')
    op.drop_table('candidate_configs')
    # ### end Alembic commands ###
