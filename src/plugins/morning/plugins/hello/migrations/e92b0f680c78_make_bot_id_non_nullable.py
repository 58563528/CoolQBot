"""make bot_id non-nullable

Revision ID: e92b0f680c78
Revises: b683352e0089
Create Date: 2023-09-30 08:57:28.404492

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e92b0f680c78"
down_revision = "b683352e0089"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("hello_hello", schema=None) as batch_op:
        batch_op.alter_column("bot_id", existing_type=sa.VARCHAR(), nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("hello_hello", schema=None) as batch_op:
        batch_op.alter_column("bot_id", existing_type=sa.VARCHAR(), nullable=True)

    # ### end Alembic commands ###