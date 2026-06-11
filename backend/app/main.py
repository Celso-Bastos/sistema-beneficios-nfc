from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.clientes import router as clientes_router
from app.api.database import router as database_router
from app.api.health import router as health_router
from app.api.nfc_tags import router as nfc_tags_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
    }


app.include_router(health_router)
app.include_router(database_router)
app.include_router(clientes_router)
app.include_router(nfc_tags_router)
