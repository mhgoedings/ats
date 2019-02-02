"""added candidate jcl version

Revision ID: 500a41b6de90
Revises: 5c3a0b080d5a
Create Date: 2018-12-30 22:51:10.529171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '500a41b6de90'
down_revision = '5c3a0b080d5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidate_configs', sa.Column('jcl_version', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('candidate_configs', 'jcl_version')
    # ### end Alembic commands ###