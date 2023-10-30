"""update lesson

Revision ID: 2fd648bdba6d
Revises: 98036de3f9f3
Create Date: 2023-10-25 23:43:29.008185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fd648bdba6d'
down_revision = '98036de3f9f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.drop_column('end_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lesson', schema=None) as batch_op:
        batch_op.add_column(sa.Column('end_at', sa.DATE(), nullable=False))

    # ### end Alembic commands ###