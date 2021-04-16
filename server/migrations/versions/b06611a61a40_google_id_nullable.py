"""google_id nullable

Revision ID: b06611a61a40
Revises: b9af22b8d7b8
Create Date: 2021-04-04 16:21:15.654267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b06611a61a40'
down_revision = 'b9af22b8d7b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('google_id', sa.String(length=64), nullable=True))
    op.create_unique_constraint(None, 'users', ['google_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'google_id')
    # ### end Alembic commands ###