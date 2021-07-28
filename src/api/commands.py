from fastapi import APIRouter, Response

from src.core.command import CommandService
from src.dependency.manager import Manager
from src.model.commands import CommandGroup
from src.model.message import response_body

router = APIRouter(prefix="/api/v1/swaddle")
command_service: CommandService = Manager.COMMAND_SERVICE


@router.post(
    "/server/commands", tags=["Commands"],
    summary="Add server commands into system"
)
async def add_command(request: CommandGroup, response: Response):
    return response_body("add_command", response, command_service.save_obj(request))


@router.get(
    "/server/commands", tags=["Commands"],
    summary="Get server commands"
)
async def get_command(response: Response, name: str = None):
    return response_body("get_command", response, command_service.search(name))
