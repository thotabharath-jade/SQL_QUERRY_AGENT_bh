from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.query import router as query_router
from app.api.history import router as history_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="SQL Query Builder Agent - Convert natural language to SQL queries",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(history_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "SQL Query Builder Agent API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
