import sys
import os
import pytest
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture(scope='session')
def test_data_dir():
    temp_dir = tempfile.mkdtemp()
    src_data_dir = os.path.join(os.path.dirname(__file__), '../src/data')
    if os.path.exists(src_data_dir):
        for file in os.listdir(src_data_dir):
            if file.endswith('.csv'):
                shutil.copy2(os.path.join(src_data_dir, file), temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def app(test_data_dir, monkeypatch):
    monkeypatch.setenv('TESTING', 'True')
    
    # Patch CSVManager to use test data directory
    from core.csv_manager import CSVManager
    monkeypatch.setattr(CSVManager(), 'data_dir', test_data_dir)
    
    from app import app as flask_app
    
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key-with-sufficient-length-for-security',
        'WTF_CSRF_ENABLED': False
    })
    
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
