# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.db_models.address import Address
from app.db_models.item import Item
from app.db_models.owner import Owner
from app.db_models.shop import Shop
from app.db_models.user import User
