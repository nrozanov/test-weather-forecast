import glob
import os
import pathlib

import pytest
from pytest_mock import MockerFixture

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

os.environ["SETTINGS_MODULE"] = "config.settings.test"


def _clean_name(val: str) -> str:
    return val.replace("/", ".").replace("\\", ".").replace(".py", "")


fixture_plugins = [
    _clean_name(name) for name in glob.glob("tests/fixtures/[!_]*.py", root_dir=BASE_DIR)
]

pytest_plugins = fixture_plugins


def pytest_addoption(parser):
    parser.addoption(
        "--schemathesis",
        action="store_true",
        default=False,
        help="run schemathesis tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "schemathesis: schemathesis tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--schemathesis"):
        return
    skip_slow = pytest.mark.skip(reason="provide --schemathesis option to run")
    for item in items:
        if "schemathesis" in item.keywords:
            item.add_marker(skip_slow)
