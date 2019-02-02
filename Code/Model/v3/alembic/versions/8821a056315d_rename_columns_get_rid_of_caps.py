"""Rename columns, get rid of caps

Revision ID: 8821a056315d
Revises: 50ed0479d68f
Create Date: 2018-10-21 09:44:24.061492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8821a056315d"
down_revision = "50ed0479d68f"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "oos_tests", "TotalNumberofTrades", nullable=True, new_column_name="trade_count"
    )
    op.alter_column(
        "oos_tests", "PercentProfitable", nullable=True, new_column_name="percent_winners"
    )
    op.alter_column(
        "oos_tests", "AvgWinningTrade", nullable=True, new_column_name="avg_winner"
    )
    op.alter_column(
        "oos_tests", "AvgLosingTrade", nullable=True, new_column_name="avg_looser"
    )
    op.alter_column(
        "oos_tests", "SharpeRatio", nullable=True, new_column_name="sharpe_ratio"
    )
    op.alter_column(
        "oos_tests", "RatioAvgWinAvgLoss", nullable=True, new_column_name="drawdown"
    )


def downgrade():
    op.alter_column(
        "oos_tests", "trade_count", nullable=True, new_column_name="TotalNumberofTrades"
    )
    op.alter_column(
        "oos_tests", "percent_winners", nullable=True, new_column_name="PercentProfitable"
    )
    op.alter_column(
        "oos_tests", "avg_winner", nullable=True, new_column_name="AvgWinningTrade"
    )
    op.alter_column(
        "oos_tests", "avg_looser", nullable=True, new_column_name="AvgLosingTrade"
    )
    op.alter_column(
        "oos_tests", "sharpe_ratio", nullable=True, new_column_name="SharpeRatio"
    )
    op.alter_column(
        "oos_tests", "drawdown", nullable=True, new_column_name="RatioAvgWinAvgLoss"
    )
