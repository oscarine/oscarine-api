"""email password_hash not nullable

Revision ID: 41a26b9d2ff9
Revises: 57f5a2ad41b0
Create Date: 2020-06-02 19:38:18.612822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41a26b9d2ff9'
down_revision = '57f5a2ad41b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('spatial_ref_sys')
    # op.drop_index('idx_address_location', table_name='address')
    op.alter_column('owner', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('owner', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # op.drop_index('idx_shops_location', table_name='shops')
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.create_index('idx_shops_location', 'shops', ['location'], unique=False)
    op.alter_column('owner', 'password_hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('owner', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
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
    # ### end Alembic commands ###
