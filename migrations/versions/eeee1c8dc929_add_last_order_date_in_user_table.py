"""Add last_order_date in User table

Revision ID: eeee1c8dc929
Revises: 345cc5f61358
Create Date: 2021-08-15 13:14:17.015880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeee1c8dc929'
down_revision = '345cc5f61358'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_order_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_order_date')
    # ### end Alembic commands ###
