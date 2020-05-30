"""addresses table

Revision ID: 2f2622a0b619
Revises: d54778171038
Create Date: 2020-05-30 14:05:03.988726

"""
from alembic import op
import sqlalchemy as sa

import geoalchemy2


# revision identifiers, used by Alembic.
revision = '2f2622a0b619'
down_revision = 'd54778171038'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('longitude', sa.Numeric(precision=15, scale=10), nullable=False),
    sa.Column('latitude', sa.Numeric(precision=15, scale=10), nullable=False),
    sa.Column('complete_address', sa.String(length=300), nullable=False),
    sa.Column('location', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326, from_text='ST_GeogFromText', name='geography'), nullable=False),
    sa.Column('tag', sa.String(length=30), nullable=False),
    sa.Column('floor', sa.String(length=50), nullable=True),
    sa.Column('landmark', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_addresses_id'), 'addresses', ['id'], unique=False)
    # op.drop_table('spatial_ref_sys')
    # op.drop_index('idx_shops_location', table_name='shops')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_shops_location', 'shops', ['location'], unique=False)
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('(srid > 0) AND (srid <= 998999)', name='spatial_ref_sys_srid_check'),
    sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    )
    op.drop_index(op.f('ix_addresses_id'), table_name='addresses')
    op.drop_table('addresses')
    # ### end Alembic commands ###
