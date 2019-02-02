"""Rename a column

Revision ID: c0c45ea44ced
Revises: 6507151dd8b1
Create Date: 2018-10-28 05:39:31.213932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0c45ea44ced"
down_revision = "6507151dd8b1"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "oos_tests", "TotalNetProfit", nullable=True, new_column_name="initial_capital"
    )
    op.alter_column(
        "oos_tests", "AvgTradeNetProfit", nullable=True, new_column_name="commission"
    )
    op.alter_column(
        "oos_tests", "ProfitFactor", nullable=True, new_column_name="slippage"
    )


def downgrade():
    op.alter_column(
        "oos_tests", "initial_capital", nullable=True, new_column_name="TotalNetProfit"
    )
    op.alter_column(
        "oos_tests", "commission", nullable=True, new_column_name="AvgTradeNetProfit"
    )
    op.alter_column(
        "oos_tests", "slippage", nullable=True, new_column_name="ProfitFactor"
    )
