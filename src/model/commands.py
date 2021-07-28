from typing import List, Optional

from pydantic import BaseModel, Field


class Command(BaseModel):
    command: str
    privileged: Optional[bool] = Field(default=False)


class CommandGroup(BaseModel):
    name: str
    type: str
    commands: List[Command]
