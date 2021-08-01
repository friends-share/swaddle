from fastapi import APIRouter

from src.dependency.manager import Manager
from src.model.server import ClusterData, ClusterDataRequest

router = APIRouter(prefix="/api/v1/swaddle")
cluster_manager = Manager.CLUSTER_MANAGER
command_manager = Manager.COMMAND_SERVICE

# @router.post(
#     "/server", tags=["Server"],
#     summary="Add servers"
# )
# async def add_cluster(request: List[Server]):
#     return server_manager.save_all(request)
#
#
# @router.get(
#     "/server", tags=["Server"],
#     summary="Get server"
# )
# async def get_cluster(server_name: str):
#     return server_manager.get_by_id(server_name)


@router.post(
    "/server/cluster", tags=["Server"],
    summary="Add server clusters"
)
async def add_cluster(request: ClusterDataRequest, group: str):
    return cluster_manager.save(request.to_cluster_data(command_manager), group)


@router.get(
    "/server/cluster", tags=["Server"],
    summary="Get server clusters"
)
async def get_cluster(cluster_id: str):
    return cluster_manager.get_by_id(cluster_id)
