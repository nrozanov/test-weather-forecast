from fastapi import FastAPI

import pytest
import schemathesis

from config.factory import create_app


@pytest.fixture
def app():
    app = create_app()

    return app


@pytest.fixture
def schema_fixture(app: FastAPI):
    return schemathesis.from_dict(app.openapi())
