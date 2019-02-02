"""Create first migration

Revision ID: 4178d4e83db9
Revises: 
Create Date: 2018-10-21 07:46:47.208860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4178d4e83db9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # market internals
    op.add_column("strategies", sa.Column("mi_id", sa.Integer(), nullable=True))
    op.add_column("strategies", sa.Column("mi_n1", sa.Integer(), nullable=True))
    op.add_column("strategies", sa.Column("mi_n2", sa.Integer(), nullable=True))

    # xact costs
    op.add_column(
        "strategies", sa.Column("comm_entry_dol", sa.Numeric(8, 4), nullable=True)
    )
    op.add_column(
        "strategies", sa.Column("comm_exit_dol", sa.Numeric(8, 4), nullable=True)
    )
    op.add_column(
        "strategies", sa.Column("slippage_entry_dol", sa.Numeric(8, 4), nullable=True)
    )
    op.add_column(
        "strategies", sa.Column("slippage_exit_dol", sa.Numeric(8, 4), nullable=True)
    )


def downgrade():
    op.drop_column("strategies", "mi_id")
    op.drop_column("strategies", "mi_n1")
    op.drop_column("strategies", "mi_n2")

    op.drop_column("strategies", "comm_entry_dol")
    op.drop_column("strategies", "comm_exit_dol")
    op.drop_column("strategies", "slippage_entry_dol")
    op.drop_column("strategies", "slippage_exit_dol")
