"""new tables  migration.

Revision ID: 738ce15c5739
Revises: 1f79269d16e8
Create Date: 2023-07-13 20:14:15.316042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '738ce15c5739'
down_revision = '1f79269d16e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exam', schema=None) as batch_op:
        batch_op.add_column(sa.Column('punctuation', sa.Integer(), nullable=True))
        batch_op.drop_column('ponctuation')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exam', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ponctuation', sa.INTEGER(), nullable=True))
        batch_op.drop_column('punctuation')

    # ### end Alembic commands ###