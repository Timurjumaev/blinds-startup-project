"""cnsjcnj

Revision ID: 835a4ec73388
Revises: ec5a17a6ded8
Create Date: 2023-07-24 17:11:02.146529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '835a4ec73388'
down_revision = 'ec5a17a6ded8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_balances',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('balance', sa.Numeric(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_balances')
    # ### end Alembic commands ###
