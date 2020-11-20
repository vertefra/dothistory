from fastapi import FastAPI

from app.routers import test_router


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(test_router.router)
    return application


app = create_application()
