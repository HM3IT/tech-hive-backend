"""Added new cols: related_context, embedding to category, phone, discount_percent_at_order to Order

Revision ID: 87aa95feae57
Revises: 
Create Date: 2024-11-20 09:55:22.827474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '87aa95feae57'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('related_context', sa.Text(), nullable=True))
    op.add_column('category', sa.Column('context_embedding', postgresql.ARRAY(sa.Float()), nullable=True))
    op.drop_column('category', 'decription')
    op.add_column('order', sa.Column('phone', sa.String(length=100), nullable=False))
    op.add_column('order_product', sa.Column('discount_percent_at_order', sa.DECIMAL(precision=5, scale=2), nullable=False))
    op.add_column('product', sa.Column('sold', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'sold')
    op.drop_column('order_product', 'discount_percent_at_order')
    op.drop_column('order', 'phone')
    op.add_column('category', sa.Column('decription', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('category', 'context_embedding')
    op.drop_column('category', 'related_context')
    # ### end Alembic commands ###