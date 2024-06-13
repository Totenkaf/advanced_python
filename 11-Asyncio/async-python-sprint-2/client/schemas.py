# Copyright (c) 2023 Artem Ustsov

from pydantic import BaseModel


class WeatherDetail(BaseModel):
    """WeatherDetail schema to parse"""

    hour: str
    temp: int
    condition: str


class Weather(BaseModel):
    """Weather schema to parse"""

    date: str
    hours: list[WeatherDetail]


class Forecast(BaseModel):
    """Forecast schema to parse"""

    forecasts: list[Weather]
