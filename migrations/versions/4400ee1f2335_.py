"""empty message

Revision ID: 4400ee1f2335
Revises: 
Create Date: 2021-08-10 20:45:22.116850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4400ee1f2335'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
