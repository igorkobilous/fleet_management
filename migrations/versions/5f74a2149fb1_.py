"""empty message

Revision ID: 5f74a2149fb1
Revises: 652708d988a4
Create Date: 2019-05-03 00:50:50.816497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f74a2149fb1'
down_revision = '652708d988a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicle', sa.Column('name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle', 'name')
    # ### end Alembic commands ###
