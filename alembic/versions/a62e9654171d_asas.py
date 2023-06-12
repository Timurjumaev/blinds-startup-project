"""asas

Revision ID: a62e9654171d
Revises: 39ca21bddb59
Create Date: 2023-06-12 13:49:35.069844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a62e9654171d'
down_revision = '39ca21bddb59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loans', 'status')
    # ### end Alembic commands ###
