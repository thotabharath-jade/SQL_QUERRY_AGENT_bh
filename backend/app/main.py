from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, query, history
from app.core.database import init_db

app = FastAPI(
    title="SQL Query Builder Agent",
    description="AI-powered SQL query builder using natural language",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(query.router)
app.include_router(history.router)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def root():
    return {
        "message": "SQL Query Builder Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
