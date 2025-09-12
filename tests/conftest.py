# tests/conftest.py
import pytest
from api import app as flask_app

@pytest.fixture()
def app():
    # se quiser, pode parametrizar configs aqui (ex.: TESTING=True)
    flask_app.config.update(TESTING=True)
    return flask_app

@pytest.fixture()
def client(app):
    return app.test_client()
