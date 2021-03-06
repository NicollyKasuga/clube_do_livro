"""created message table

Revision ID: 08a369aa4314
Revises: 772f9fde22e0
Create Date: 2022-04-28 19:28:01.792575

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "08a369aa4314"
down_revision = "772f9fde22e0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "messages",
        sa.Column("message_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sender_id", postgresql.UUID(), nullable=False),
        sa.Column("reciever_id", postgresql.UUID(), nullable=False),
        sa.Column("message_text", sa.String(length=600), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["reciever_id"],
            ["readers.reader_id"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["readers.reader_id"],
        ),
        sa.PrimaryKeyConstraint("message_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("messages")
    # ### end Alembic commands ###
