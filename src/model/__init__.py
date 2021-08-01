from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Grouped(BaseModel):
    group: str


class Level(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0


class Credential(BaseModel):
    name: str
    password: Optional[str]
    secret_key: Optional[str]


class InfraCharacteristic(BaseModel):
    cpu: Optional[Level] = Field(default=Level.MEDIUM)
    gpu: Optional[Level] = Field(default=Level.NONE)
    network: Optional[Level] = Field(default=Level.MEDIUM)
    io: Optional[Level] = Field(default=Level.MEDIUM)

    def match(self, other) -> bool:
        return isinstance(other, InfraCharacteristic) and \
               self.cpu.value >= other.cpu.value and \
               self.gpu.value >= other.gpu.value and \
               self.io.value >= other.io.value and \
               self.network.value >= other.network.value


class GitRepo(BaseModel):
    repo: str
    credential: Optional[Credential]
