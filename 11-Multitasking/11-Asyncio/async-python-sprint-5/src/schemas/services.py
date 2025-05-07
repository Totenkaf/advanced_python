from pydantic import BaseModel


class Ping(BaseModel):
    db: float
    cache: float
