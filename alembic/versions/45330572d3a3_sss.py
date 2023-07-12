"""sss

Revision ID: 45330572d3a3
Revises: 47ddc6410773
Create Date: 2023-07-11 20:46:15.269885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45330572d3a3'
down_revision = '47ddc6410773'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stage_users', sa.Column('currency_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stage_users', 'currency_id')
    # ### end Alembic commands ###