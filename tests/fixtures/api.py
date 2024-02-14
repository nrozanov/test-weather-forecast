from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
