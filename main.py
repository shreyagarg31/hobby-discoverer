from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, hobby_router
from contextlib import asynccontextmanager
from app.config.settings import MongoManager
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoManager.connect()
    yield
    await MongoManager.close()

app = FastAPI(title="Hobby Discoverer API", lifespan=lifespan)

@app.middleware("http")
async def exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(e)}
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["users"])
app.include_router(hobby_router.router, prefix=settings.API_V1_PREFIX, tags=["hobbies"])
# @app.on_event("startup")
# async def startup_db_client():
#     print("Starting the app")
#     MongoManager.connect()

# @app.on_event("shutdown")
# async def shutdown_db_client():
#    MongoManager.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}
