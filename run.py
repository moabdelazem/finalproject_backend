from fastapi import FastAPI
from app.routes import router
from app.db.database import create_tables
from fastapi.middleware.cors import CORSMiddleware

# Create a new FastAPI instance
app = FastAPI()
# Include the router in the app
app.include_router(router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins. Change this to restrict to specific domains.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Initialize the database
def init_db():
    create_tables()


if __name__ == "__main__":
    # Initialize the database on run
    init_db()
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
