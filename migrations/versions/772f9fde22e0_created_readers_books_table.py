"""created readers books table

Revision ID: 772f9fde22e0
Revises: 60fa870e7187
Create Date: 2022-04-28 19:20:58.390029

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '772f9fde22e0'
down_revision = '60fa870e7187'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('reader_book_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('reader_id', postgresql.UUID(), nullable=False),
    sa.Column('book_id', postgresql.UUID(), nullable=False),
    sa.Column('review', sa.String(length=200), nullable=True),
    sa.Column('rating', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['reader_id'], ['readers.reader_id'], ),
    sa.PrimaryKeyConstraint('reader_book_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    # ### end Alembic commands ###
