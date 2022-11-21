from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app import crud, sqlmodels
from app.api import deps

router = APIRouter()
