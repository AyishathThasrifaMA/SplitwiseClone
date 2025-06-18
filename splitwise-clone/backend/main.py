from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import groups, expenses, users
from database import engine, Base

app = FastAPI()

# CORS setup for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Splitwise clone backend is running"}
