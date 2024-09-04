from fastapi import APIRouter

# Create a new APIRouter instance
router = APIRouter()

# Import the user and book routers
from .user import router as user_router
from .book import router as book_router

# Include the user and book routers in the main router
router.include_router(user_router, prefix="/users")
router.include_router(book_router, prefix="/books")
