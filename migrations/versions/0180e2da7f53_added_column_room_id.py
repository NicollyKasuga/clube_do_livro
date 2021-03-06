"""added column room_id

Revision ID: 0180e2da7f53
Revises: 32588dc02189
Create Date: 2022-04-30 23:07:16.091313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0180e2da7f53'
down_revision = '32588dc02189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('room_id', postgresql.UUID(), nullable=False))
    op.create_foreign_key(None, 'messages', 'rooms', ['room_id'], ['room_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.drop_column('messages', 'room_id')
    # ### end Alembic commands ###
