from pydantic import BaseModel


class ScaleRequest(BaseModel):
    name: str
    count: int
