"""question table migration.

Revision ID: 0d7ae29a9231
Revises: 813e9f25be18
Create Date: 2023-07-19 12:01:40.828454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d7ae29a9231'
down_revision = '813e9f25be18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('json_alternatives', sa.JSON(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.drop_column('json_alternatives')

    # ### end Alembic commands ###