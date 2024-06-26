"""empty message

Revision ID: 379e253a62b0
Revises: d52b3d6f8779
Create Date: 2024-05-23 20:27:09.375427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '379e253a62b0'
down_revision = 'd52b3d6f8779'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('etd',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=True),
    sa.Column('prenom', sa.String(length=100), nullable=True),
    sa.Column('contact', sa.String(length=100), nullable=True),
    sa.Column('carte_number', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('etudiant')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('etudiant',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('nom', sa.VARCHAR(length=100), nullable=False),
    sa.Column('prenom', sa.VARCHAR(length=100), nullable=False),
    sa.Column('contact', sa.VARCHAR(length=20), nullable=False),
    sa.Column('etudiant_id', sa.VARCHAR(length=20), nullable=False),
    sa.Column('classe', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('etudiant_id')
    )
    op.drop_table('etd')
    # ### end Alembic commands ###
