import pathlib

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from a2wsgi import WSGIMiddleware
from fastapi_pagination import add_pagination

from config import routers
from config.settings import settings
from config.weather_data import WeatherData


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title="Test server for weather forecast",
    )

    routers.init_app(app)
    add_pagination(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup_event():
        WeatherData()

    return app
