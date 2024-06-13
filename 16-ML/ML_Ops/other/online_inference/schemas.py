from typing import Literal

from pydantic import BaseModel, validator


class MedicalData(BaseModel):
    age: float
    sex: Literal[0, 1]
    cp: Literal[0, 1, 2, 3]
    trestbps: float
    chol: float
    fbs: Literal[0, 1]
    restecg: Literal[0, 1, 2]
    thalach: float
    exang: Literal[0, 1]
    oldpeak: float
    slope: Literal[0, 1, 2]
    ca: Literal[0, 1, 2, 3]
    thal: Literal[0, 1, 2]

    @validator('age')
    def age_validator(cls, v):
        if v < 0 or v > 100:
            raise ValueError('wrong age value')
        return v

    @validator('trestbps')
    def trestbps_validator(cls, v):
        if v < 0 or v > 250:
            raise ValueError('wrong trestbps value')
        return v

    @validator('chol')
    def chol_validator(cls, v):
        if v < 0 or v > 700:
            raise ValueError('wrong chol value')
        return v

    @validator('thalach')
    def thalach_validator(cls, v):
        if v < 0 or v > 250:
            raise ValueError('wrong thalach value')
        return v

    @validator('oldpeak')
    def oldpeak_validator(cls, v):
        if v < 0 or v > 8:
            raise ValueError('wrong oldpeak value')
        return v
