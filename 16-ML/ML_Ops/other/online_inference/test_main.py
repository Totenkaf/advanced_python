import json

import pytest
from fastapi.testclient import TestClient

from main import app, load_model

client = TestClient(app)


@pytest.fixture(scope='session', autouse=True)
def initialize_model():
    load_model()


def test_predict_endpoint():
    request = {
        'age': 53,
        'sex': 0,
        'cp': 3,
        'trestbps': 155,
        'chol': 165,
        'fbs': 1,
        'restecg': 0,
        'thalach': 91,
        'exang': 0,
        'oldpeak': 1.7,
        'slope': 0,
        'ca': 0,
        'thal': 2
        }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 200
    assert response.json() == {'condition': 'sick'}


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == 'Model is ready'


def test_missing_fields():
    request = {
        'age': 53,
        'sex': 0,
        'cp': 3,
        'trestbps': 155,
        'chol': 165,
        'fbs': 1,
        'restecg': 0,
        'thalach': 91,
        'exang': 0,
        'oldpeak': 1.7,
        'slope': 0,
        'thal': 2
        }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'field required'


def test_categorical_fields():
    request = {
        'age': 53,
        'sex': 2,
        'cp': 3,
        'trestbps': 155,
        'chol': 165,
        'fbs': 1,
        'restecg': 0,
        'thalach': 91,
        'exang': 0,
        'oldpeak': 1.7,
        'slope': 0,
        'ca': 0,
        'thal': 2
        }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'unexpected value; permitted: 0, 1'


def test_numerical_fields():
    request = {
        'age': 530,
        'sex': 1,
        'cp': 3,
        'trestbps': 155,
        'chol': 165,
        'fbs': 1,
        'restecg': 0,
        'thalach': 91,
        'exang': 0,
        'oldpeak': 1.7,
        'slope': 0,
        'ca': 0,
        'thal': 2
        }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'wrong age value'
