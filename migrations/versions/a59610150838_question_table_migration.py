"""question table migration.

Revision ID: a59610150838
Revises: 0d7ae29a9231
Create Date: 2023-07-19 22:29:19.550704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59610150838'
down_revision = '0d7ae29a9231'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qty_alternatives', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('qty_alternatives')

    # ### end Alembic commands ###