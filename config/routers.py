from fastapi.applications import FastAPI

import weather.api.routes


def init_app(app: FastAPI) -> None:
    app.include_router(
        weather.api.routes.router,
        prefix="/weather",
        tags=["weather"],
    )
