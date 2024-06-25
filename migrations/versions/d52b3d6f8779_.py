"""empty message

Revision ID: d52b3d6f8779
Revises: 0c7ebb434c73
Create Date: 2024-05-23 17:26:24.053010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd52b3d6f8779'
down_revision = '0c7ebb434c73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('etudiant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=False),
    sa.Column('prenom', sa.String(length=100), nullable=False),
    sa.Column('contact', sa.String(length=20), nullable=False),
    sa.Column('etudiant_id', sa.String(length=20), nullable=False),
    sa.Column('classe', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('etudiant_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('etudiant')
    # ### end Alembic commands ###
