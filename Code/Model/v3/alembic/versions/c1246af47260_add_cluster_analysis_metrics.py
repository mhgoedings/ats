"""add cluster analysis metrics

Revision ID: c1246af47260
Revises: 56d07a659137
Create Date: 2018-11-13 10:22:38.885022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c1246af47260"
down_revision = "56d07a659137"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("strategies", sa.Column("profit_ring_1", sa.Integer, nullable=True))
    op.add_column("strategies", sa.Column("profit_ring_2", sa.Integer, nullable=True))
    op.add_column(
        "strategies", sa.Column("profit_ring_center", sa.Integer, nullable=True)
    )
    op.add_column("strategies", sa.Column("wfe_ring_1", sa.Integer, nullable=True))
    op.add_column("strategies", sa.Column("wfe_ring_2", sa.Integer, nullable=True))
    op.add_column("strategies", sa.Column("wfe_ring_center", sa.Integer, nullable=True))
    op.add_column(
        "strategies", sa.Column("consistency_ring_1", sa.Integer, nullable=True)
    )
    op.add_column(
        "strategies", sa.Column("consistency_ring_2", sa.Integer, nullable=True)
    )
    op.add_column(
        "strategies", sa.Column("consistency_ring_center", sa.Integer, nullable=True)
    )


def downgrade():
    op.drop_column("strategies", "profit_ring_1")
    op.drop_column("strategies", "profit_ring_2")
    op.drop_column("strategies", "profit_ring_center")
    op.drop_column("strategies", "wfe_ring_1")
    op.drop_column("strategies", "wfe_ring_2")
    op.drop_column("strategies", "wfe_ring_center")
    op.drop_column("strategies", "consistency_ring_1")
    op.drop_column("strategies", "consistency_ring_2")
    op.drop_column("strategies", "consistency_ring_center")
