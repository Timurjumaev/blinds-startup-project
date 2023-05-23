"""salom

Revision ID: e508c11dbf1f
Revises: 1c7e79340ec8
Create Date: 2023-05-23 17:19:37.829638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e508c11dbf1f'
down_revision = '1c7e79340ec8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loans',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('money', sa.Numeric(), nullable=True),
    sa.Column('residual', sa.Numeric(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.Column('comment', sa.String(length=999), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('standart_mechanisms',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mechanism_id', sa.Integer(), nullable=True),
    sa.Column('width', sa.Numeric(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trade_mechanisms',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trade_id', sa.Integer(), nullable=True),
    sa.Column('mechanism_id', sa.Integer(), nullable=True),
    sa.Column('width', sa.Numeric(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('material_id', sa.Integer(), nullable=True),
    sa.Column('width', sa.Numeric(), nullable=True),
    sa.Column('height', sa.Numeric(), nullable=True),
    sa.Column('stage_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('comment', sa.String(length=999), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('uploaded_files',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file', sa.String(length=999), nullable=True),
    sa.Column('source', sa.String(length=999), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=999), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('uploaded_files')
    op.drop_table('trades')
    op.drop_table('trade_mechanisms')
    op.drop_table('standart_mechanisms')
    op.drop_table('loans')
    # ### end Alembic commands ###
