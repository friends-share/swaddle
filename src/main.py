from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from src.api.apps import router as apps
from src.api.commands import router as commands
from src.api.deploy import router as deployer
from src.api.scale import router as scaler
from src.api.server import router as server
from src.system_hook import System
from src.api.files import router as file_api

app = FastAPI(
    title="Swaddle",
    description="Deploy without care",
    version="0.1.0"
)

logger.add("./logs/swaddle.log", rotation="5 MB")
logger.info(f"Initializing {app.title}.v{app.version}...")

logger.info("Adding apps namespace route")
app.include_router(apps)
logger.info("Adding server namespace route")
app.include_router(server)
logger.info("Adding deployer namespace route")
app.include_router(deployer)
logger.info("Adding scaler namespace route")
app.include_router(scaler)
logger.info("Adding command namespace route")
app.include_router(commands)
logger.info("Adding files namespace route")
app.include_router(file_api)


@app.on_event("startup")
def startup():
    System.on_start()


@app.on_event("shutdown")
def startup():
    System.on_stop()


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")
