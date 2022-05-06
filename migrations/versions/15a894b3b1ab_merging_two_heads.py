"""merging two heads

Revision ID: 15a894b3b1ab
Revises: 6f474bb4571e, 9a67c8067d0a
Create Date: 2022-05-05 08:43:19.892202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15a894b3b1ab'
down_revision = ('6f474bb4571e', '9a67c8067d0a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
