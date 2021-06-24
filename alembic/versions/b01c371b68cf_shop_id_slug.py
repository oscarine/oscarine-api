"""shop id slug

Revision ID: b01c371b68cf
Revises: ea97318f0bc6
Create Date: 2021-06-17 22:32:03.226903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b01c371b68cf'
down_revision = 'ea97318f0bc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.execute('ALTER TABLE public.order DROP CONSTRAINT order_shop_id_fkey')
    op.execute('ALTER TABLE public.order ALTER COLUMN shop_id TYPE varchar(100)')

    op.execute('ALTER TABLE items DROP CONSTRAINT items_shop_id_fkey')
    op.execute('ALTER TABLE items ALTER COLUMN shop_id TYPE varchar(100)')

    op.execute('ALTER TABLE cart DROP CONSTRAINT cart_shop_id_fkey')
    op.execute('ALTER TABLE cart ALTER COLUMN shop_id TYPE varchar(100)')

    op.execute('ALTER TABLE shops ALTER COLUMN id TYPE varchar(100)')

    op.execute('ALTER TABLE public.order ADD CONSTRAINT order_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES shops (id)')

    op.execute('ALTER TABLE items ADD CONSTRAINT items_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES shops (id)')

    op.execute('ALTER TABLE cart ADD CONSTRAINT cart_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES shops (id)')
    # ### end Alembic commands ###


# def downgrade():
#     # ### commands auto generated by Alembic - please adjust! ###

#     # ### end Alembic commands ###
