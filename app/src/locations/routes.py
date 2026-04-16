from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from http import HTTPStatus
from .service import LocationService
from .schemas import LocationResponseModel, LocationCreateModel

locations_router = APIRouter(prefix="/locations")

# LOCATIONS METHODS --------------------------------------------

@locations_router.get("/", response_model=List[LocationResponseModel]) 
async def read_locations(session: AsyncSession = Depends(get_session)):
    """
    Retrieves all locations from the database.

    Args:
        session (AsyncSession): The database session.

    Returns:
        List[LocationResponseModel]: A list of all locations.
    """
    locations = await LocationService(session).get_all_locations()
    return locations

# Modify for cases where the id is: not found / incorrect length (37 characters)
@locations_router.get("/{location_id}", status_code=HTTPStatus.OK)
async def read_location(location_id: str, session: AsyncSession = Depends(get_session)):
    """
    Retrieves a specific location by its unique identifier.

    Args:
        location_id (str): The UUID of the location.
        session (AsyncSession): The database session.

    Returns:
        LocationResponseModel: The requested location.
    """
    location = await LocationService(session).get_location(location_id)
    return location

@locations_router.post("/", status_code=HTTPStatus.CREATED)
async def create_location(
    location_create_data: LocationCreateModel, session: AsyncSession = Depends(get_session)
):
    """
    Creates a new location record.

    Args:
        location_create_data (LocationCreateModel): The data for the new location.
        session (AsyncSession): The database session.

    Returns:
        LocationResponseModel: The newly created location.
    """
    new_location = await LocationService(session).create_location(location_create_data)

    return new_location

# Modify for cases where the id is: not found / incorrect length (37 characters)
# Modify to update the update attribute 
@locations_router.put("/{location_id}", status_code=HTTPStatus.OK)
async def update_location(
    location_id: str,
    update_data: LocationCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """
    Updates an existing location record.

    Args:
        location_id (str): The UUID of the location to update.
        update_data (LocationCreateModel): The new data for the location.
        session (AsyncSession): The database session.

    Returns:
        LocationResponseModel: The updated location.
    """
    updated_location = await LocationService(session).update_location(location_id, update_data)

    return updated_location

@locations_router.delete("/{location_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_location(location_id: str, session: AsyncSession = Depends(get_session)):
    """
    Deletes a location record by its unique identifier.

    Args:
        location_id (str): The UUID of the location to delete.
        session (AsyncSession): The database session.

    Returns:
        dict: An empty dictionary indicating successful deletion.
    """
    await LocationService(session).delete_location(location_id)
    return {}