from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ExcludeConstraint

from app.db.base_class import Base


class Cart(Base):
    """
    To store the items in cart
    """

    __table_args__ = (
        UniqueConstraint('item_id', 'user_id', name='_item_user_uc'),
        ExcludeConstraint(
            (Column('user_id'), '='),
            (Column('shop_id'), '<>'),
        ),
    )

    """Exclude constraint is used which enforce the rule that a user in a cart
    can contain only one shop. See here: https://www.postgresql.org/docs/9.2/btree-gist.html#AEN146719
    and, https://stackoverflow.com/a/51247705/10305905

    Unique constraint is added to enforce that a user cannot add two rows with same item_id
    """

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False, index=True)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    item_quantity = Column(Integer, default=1, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
