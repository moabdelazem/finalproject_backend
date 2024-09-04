from fastapi import FastAPI
from app.routes import router
from app.db.database import create_tables

# Create a new FastAPI instance
app = FastAPI()
# Include the router in the app
app.include_router(router)


# Initialize the database
def init_db():
    create_tables()


if __name__ == "__main__":
    # Initialize the database on run
    init_db()
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
