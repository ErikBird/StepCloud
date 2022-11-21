from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app import crud, sqlmodels
from app.api import deps

router = APIRouter()


@router.post("/", response_model=sqlmodels.IdentifierReadWithDevices)
async def create_identifier(
        *,
        db: AsyncSession = Depends(deps.async_get_db),
        identifier_in: sqlmodels.IdentifierCreate,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    identifier = await crud.identifier.get_by_expression(db, expression=identifier_in.expression)
    if identifier:
        raise HTTPException(
            status_code=400,
            detail="A identifier object with this expression already exists in the system.",
        )
    db_identifier = sqlmodels.Identifier.from_orm(identifier_in)
    db.add(db_identifier)
    await db.commit()
    await db.refresh(db_identifier)
    return db_identifier


@router.get("/", response_model=List[sqlmodels.Identifier])
async def read_identifiers(
        db: AsyncSession = Depends(deps.async_get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: sqlmodels.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    identifier = await crud.identifier.get_multi(db, skip=skip, limit=limit)

    return identifier
