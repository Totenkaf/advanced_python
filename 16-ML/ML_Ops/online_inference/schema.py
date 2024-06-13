"""Copyright 2022 by Artem Ustsov"""

from typing import Literal

from pydantic import BaseModel, validator


class MedicalFeatures(BaseModel):
    age: float
    sex: Literal[0, 1]
    chest_pain_type: Literal[0, 1, 2, 3]
    resting_blood_pressure: float
    cholesterol: float
    fasting_blood_sugar: Literal[0, 1]
    rest_ecg: Literal[0, 1, 2]
    max_heart_rate_achieved: float
    exercise_induced_angina: Literal[0, 1]
    st_depression: float
    st_slope: Literal[0, 1, 2]
    num_major_vessels: float
    thalassemia: Literal[0, 1, 2]

    @validator('age')
    def age_validator(cls, v):
        if v < 0 or v > 80:
            raise ValueError('Wrong age')
        return v

    @validator('resting_blood_pressure')
    def resting_blood_pressure_validator(cls, v):
        if v < 0 or v > 200:
            raise ValueError('Wrong resting blood pressure')
        return v

    @validator('max_heart_rate_achieved')
    def max_heart_rate_achieved_validator(cls, v):
        if v < 0 or v > 250:
            raise ValueError('Wrong maximum heart rate')
        return v

    @validator('cholesterol')
    def cholesterol_validator(cls, v):
        if v < 0 or v > 700:
            raise ValueError('Wrong cholesterol value')
        return v

    @validator('num_major_vessels')
    def num_major_vessels_validator(cls, v):
        if v < 0 or v > 8:
            raise ValueError('Wrong oldpeak value')
        return v

    @validator('thalassemia')
    def thalassemia_validator(cls, v):
        if v < 0 or v > 250:
            raise ValueError('Wrong thalassemia value')
        return v
