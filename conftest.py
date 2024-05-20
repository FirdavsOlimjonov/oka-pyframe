import pytest
from app import OkaFrameApp


@pytest.fixture
def app():
    return OkaFrameApp()


@pytest.fixture
def test_client(app):
    return app.test_session()
