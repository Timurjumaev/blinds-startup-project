"""salom

Revision ID: 6b8442f97299
Revises: 8d7400a64251
Create Date: 2023-05-24 18:21:55.453355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b8442f97299'
down_revision = '8d7400a64251'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('warehouse_materials', sa.Column('width', sa.Numeric(), nullable=True))
    op.add_column('warehouse_materials', sa.Column('height', sa.Numeric(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('warehouse_materials', 'height')
    op.drop_column('warehouse_materials', 'width')
    # ### end Alembic commands ###