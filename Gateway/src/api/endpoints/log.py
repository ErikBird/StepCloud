from fastapi import APIRouter
from src.constants.const import System

router = APIRouter()


@router.get("/error", response_model=list[str])
async def all_manual_interfaces():
    with open(System.LOGGING_PATH_ERROR) as f:
        lines = []
        for line in f.readlines():
            lines.append(line.replace('\n', ''))
        return lines
