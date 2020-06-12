"""order and ordered_item tables

Revision ID: db26174ec486
Revises: 41a26b9d2ff9
Create Date: 2020-06-03 18:00:02.669527

"""
from alembic import op
import sqlalchemy as sa

import sqlalchemy_utils
from app.choices.order_status import ORDER_STATUS_TYPES


# revision identifiers, used by Alembic.
revision = 'db26174ec486'
down_revision = '41a26b9d2ff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_datetime', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('user_instructions', sa.String(length=150), nullable=True),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(ORDER_STATUS_TYPES, impl=sa.String(length=20)), nullable=False),
    sa.Column('total_cost', sa.Numeric(scale=2), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.create_table('ordered_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Numeric(scale=2), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ordered_item_id'), 'ordered_item', ['id'], unique=False)
    # op.drop_table('spatial_ref_sys')
    # op.drop_index('idx_address_location', table_name='address')
    # op.drop_index('idx_shops_location', table_name='shops')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_shops_location', 'shops', ['location'], unique=False)
    op.create_index('idx_address_location', 'address', ['location'], unique=False)
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    op.drop_index(op.f('ix_ordered_item_id'), table_name='ordered_item')
    op.drop_table('ordered_item')
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    # ### end Alembic commands ###
