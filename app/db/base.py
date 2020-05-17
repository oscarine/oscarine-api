# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.db_models.user import User
from app.db_models.owner import Owner
from app.db_models.shop import Shop
