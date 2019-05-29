"""added student_test score

Revision ID: e757280228e7
Revises: 7bafdfc4dbce
Create Date: 2019-05-29 10:34:03.166938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e757280228e7'
down_revision = '7bafdfc4dbce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_test', sa.Column('score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student_test', 'score')
    # ### end Alembic commands ###