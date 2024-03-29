"""empty message

Revision ID: 668e133e201a
Revises: 06178a9a326c
Create Date: 2019-11-07 16:14:46.552181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '668e133e201a'
down_revision = '06178a9a326c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('university_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['university_id'], ['universities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_email'), 'students', ['email'], unique=True)
    op.create_index(op.f('ix_students_first_name'), 'students', ['first_name'], unique=False)
    op.create_index(op.f('ix_students_last_name'), 'students', ['last_name'], unique=False)
    op.create_index(op.f('ix_students_username'), 'students', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_students_username'), table_name='students')
    op.drop_index(op.f('ix_students_last_name'), table_name='students')
    op.drop_index(op.f('ix_students_first_name'), table_name='students')
    op.drop_index(op.f('ix_students_email'), table_name='students')
    op.drop_table('students')
    # ### end Alembic commands ###
