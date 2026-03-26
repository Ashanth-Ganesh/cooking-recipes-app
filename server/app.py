from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateways.database.database import Database
from routers import auth, recipes, favorites
from services.shared.logger import logger

db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Cooking Recipes API…")
    db.init_db()
    logger.info("Database tables verified.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Cooking Recipes API",
    description="Recipe search, filtering, and favorites powered by Spoonacular",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(recipes.router, prefix="/api/recipes")
app.include_router(favorites.router, prefix="/api/favorites")


@app.get("/")
def root():
    return {"message": "Cooking Recipes API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}
