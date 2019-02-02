"""alter entry_filters columns

Revision ID: ecf9bf739e6e
Revises: c65b4a226165
Create Date: 2018-12-16 23:57:15.426491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecf9bf739e6e'
down_revision = 'c65b4a226165'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('entry_filters', 'common_logic',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=True)
    op.alter_column('entry_filters', 'filter_type',
               existing_type=sa.VARCHAR(length=12),
               type_=sa.String(length=32),
               existing_nullable=True)
    op.alter_column('entry_filters', 'long_logic',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=256),
               existing_nullable=True)
    op.alter_column('entry_filters', 'short_logic',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=256),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('entry_filters', 'short_logic',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('entry_filters', 'long_logic',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('entry_filters', 'filter_type',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=12),
               existing_nullable=True)
    op.alter_column('entry_filters', 'common_logic',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###
