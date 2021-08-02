import os
from pathlib import Path

from fastapi import UploadFile, File

Path("vault").mkdir(parents=True, exist_ok=True)


async def put(file: UploadFile = File(...)):
    filename = os.path.join("vault", file.filename)
    with open(filename, "wb+") as file_object:
        file_object.write(file.file.read())
    os.chmod(filename, 0o400)
    return filename


def get(file: str):
    return os.path.join("vault", file)
