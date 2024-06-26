"""empty message

Revision ID: 0c7ebb434c73
Revises: 
Create Date: 2024-05-22 13:36:01.813366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c7ebb434c73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enseignant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('matricule', sa.String(length=20), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=False),
    sa.Column('contact', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('matricule')
    )
    op.create_table('seance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classe', sa.String(length=10), nullable=False),
    sa.Column('matiere', sa.String(length=100), nullable=False),
    sa.Column('jour', sa.String(length=10), nullable=False),
    sa.Column('heure', sa.String(length=20), nullable=False),
    sa.Column('nom_enseignant', sa.String(length=100), nullable=False),
    sa.Column('contact_enseignant', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('seance')
    op.drop_table('enseignant')
    # ### end Alembic commands ###
