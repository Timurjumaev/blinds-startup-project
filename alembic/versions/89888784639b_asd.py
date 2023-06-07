"""asd

Revision ID: 89888784639b
Revises: 6b8442f97299
Create Date: 2023-06-03 14:26:28.095474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89888784639b'
down_revision = '6b8442f97299'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('currency_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loans', 'currency_id')
    # ### end Alembic commands ###