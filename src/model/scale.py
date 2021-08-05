from pydantic import BaseModel


class ScaleRequest(BaseModel):
    app_name: str
    group: str
    count: int
