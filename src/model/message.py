from enum import Enum
from typing import List, Optional, TypeVar

from pydantic import BaseModel
from fastapi import Response, status

Data = TypeVar('Data')


class Status(Enum):
    STARTED = status.HTTP_201_CREATED
    RUNNING = status.HTTP_202_ACCEPTED
    SUCCESS = status.HTTP_200_OK
    FAILURE = status.HTTP_500_INTERNAL_SERVER_ERROR
    FAILURE_DATA_ISSUE = status.HTTP_400_BAD_REQUEST
    COMPLETED_WITH_WARN = 211
    COMPLETED_WITH_FAILURES = 212


class MinStatus(Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    NOT_STARTED = "NOT STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class SimpleStatus(BaseModel):
    status: MinStatus
    errors: Optional[List[str]]
    messages: Optional[List[str]]


class ProcessStatus(SimpleStatus):
    data: Optional[Data]
    status: Status
    errors: Optional[List[str]]
    messages: Optional[List[str]]


class CmdResponse(ProcessStatus):
    command: str


def response_body(command, prcs_status: Status, response: Response, data: Data = None, messages: [str] = None,
                  errors: [str] = None):
    response.status_code = prcs_status.value
    return CmdResponse(command=command, status=prcs_status, data=data, messages=messages, errors=errors)


def response_body(command, response: Response, prcs_status: ProcessStatus):
    response.status_code = prcs_status.status.value
    return CmdResponse(command=command, status=prcs_status.status, data=prcs_status.data, messages=prcs_status.messages,
                       errors=prcs_status.errors)
