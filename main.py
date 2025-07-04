from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from src.settings.config import engine, get_db, settings
from src.database import models
from src.auth.routes import router as auth_router
from src.routers.contacts import router as contacts_router
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from src.routers.users import router as users_router
from fastapi.openapi.utils import get_openapi
from src.routers import auth


# models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI(title="Contacts API HW12")
app.include_router(auth_router)
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
  
    r = await redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


    models.Base.metadata.create_all(bind=engine)

@app.get("/", name="API root")
def get_index():
    return {"message": "Welcome to contacts API NATA12"}


@app.get("/health", name="Service availability")
def get_health_status(db=Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1+1")).fetchone()
        if result is None:
            raise Exception
        return {"message": "API Nata12 is ready to work"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database is not available")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Contacts API HW10",
        version="1.0.0",
        description="API for managing contacts with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":

    models.Base.metadata.create_all(bind=engine)