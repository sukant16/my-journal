"""post to post_filename

Revision ID: d96697917d8e
Revises: 34635fc9c200
Create Date: 2021-03-27 16:19:11.582232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd96697917d8e'
down_revision = '34635fc9c200'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('post_filename', sa.String(length=5000), nullable=True))
    op.drop_column('posts', 'post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('post', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('posts', 'post_filename')
    # ### end Alembic commands ###
