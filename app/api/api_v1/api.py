from fastapi import APIRouter

from app.api.api_v1.endpoints import address, items, login, orders, owner, shops, users

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(owner.router, tags=["owner"])
api_router.include_router(shops.router, tags=["shops"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(orders.router, tags=["orders"])
api_router.include_router(address.router, tags=["addresses"])
