from fastapi import FastAPI
from routes import router
from database import Base, engine

app = FastAPI()
# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(router)

@app.get("/")  # Test endpoint
def home():
    return {"message": "FastAPI is running"}




'''
    fastapi_auth_service/
    │── main.py                # Entry point of the FastAPI app
    │── database.py            # Database connection
    │── models.py              # SQLAlchemy models
    │── schemas.py             # Pydantic models for request/response validation
    │── routes.py              # API routes (register, login, etc.)
    │── requirements.txt       # List of required packages
    │── __init__.py            # Makes this a Python package

'''