import json

import pytest
from fastapi.testclient import TestClient

from main import app, load_model

client = TestClient(app)


@pytest.fixture(scope='session', autouse=True)
def initialize_model():
    load_model()


def test_predict_disease_endpoint():
    request = {
        "age": 59,
        "sex": 1,
        "chest_pain_type": 0,
        "resting_blood_pressure": 170,
        "cholesterol": 288,
        "fasting_blood_sugar": 0,
        "rest_ecg": 2,
        "max_heart_rate_achieved": 159,
        "exercise_induced_angina": 0,
        "st_depression": 0.2,
        "st_slope": 1,
        "num_major_vessels": 0,
        "thalassemia": 2,
    }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 200
    assert response.json() == {'condition': 'disease'}


def test_predict_no_disease_endpoint():
    request = {
        "age": 69,
        "sex": 0,
        "chest_pain_type": 0,
        "resting_blood_pressure": 160,
        "cholesterol": 234,
        "fasting_blood_sugar": 1,
        "rest_ecg": 2,
        "max_heart_rate_achieved": 131,
        "exercise_induced_angina": 0,
        "st_depression": 0.1,
        "st_slope": 1,
        "num_major_vessels": 1,
        "thalassemia": 0,
    }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 200
    assert response.json() == {'condition': 'no disease'}


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == 'Model is ready'


def test_missing_fields():
    request = {
        "age": 69,
        "sex": 1,
        "chest_pain_type": 0,
        "resting_blood_pressure": 160,
        "cholesterol": 234,
        "fasting_blood_sugar": 1,
        "rest_ecg": 2,
        "max_heart_rate_achieved": 131,
        "exercise_induced_angina": 0,
        "st_depression": 0.1,
        "st_slope": 1,
        "num_major_vessels": 1,
    }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'field required'


def test_categorical_fields():
    request = {
        "age": 69,
        "sex": 1,
        "chest_pain_type": 0,
        "resting_blood_pressure": 160,
        "cholesterol": 234,
        "fasting_blood_sugar": 1,
        "rest_ecg": 2,
        "max_heart_rate_achieved": 131,
        "exercise_induced_angina": 0,
        "st_depression": 0.1,
        "st_slope": 1,
        "num_major_vessels": 1,
        "thalassemia": 10,
    }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'unexpected value; permitted: 0, 1, 2'


def test_numerical_fields():
    request = {
        "age": 777,
        "sex": 1,
        "chest_pain_type": 0,
        "resting_blood_pressure": 160,
        "cholesterol": 234,
        "fasting_blood_sugar": 1,
        "rest_ecg": 2,
        "max_heart_rate_achieved": 131,
        "exercise_induced_angina": 0,
        "st_depression": 0.1,
        "st_slope": 1,
        "num_major_vessels": 1,
        "thalassemia": 0,
    }
    response = client.post(
        '/predict',
        json.dumps(request)
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Wrong age'