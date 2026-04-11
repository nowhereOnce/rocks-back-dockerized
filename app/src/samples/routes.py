from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from http import HTTPStatus
from .service import SampleService
from .schemas import SampleCreateModel, SampleResponseModel
from src.auth import get_current_active_user

samples_router = APIRouter(prefix="/samples")

# SAMPLES METHODS --------------------------------------------

@samples_router.get("/", response_model=List[SampleResponseModel]) 
async def read_samples(session: AsyncSession = Depends(get_session)):
    """
    Retrieves all samples from the database, including their associated rock and location data.

    Args:
        session (AsyncSession): The database session.

    Returns:
        List[SampleResponseModel]: A list of all samples with detailed information.
    """
    samples = await SampleService(session).get_all_samples()
    return samples

# modify for cases where the id is: not found / incorrect length (37 characters)
@samples_router.get("/{sample_id}", status_code=HTTPStatus.OK)
async def read_sample(sample_id: str, session: AsyncSession = Depends(get_session)):
    """
    Retrieves a specific sample by its unique identifier.

    Args:
        sample_id (str): The UUID of the sample.
        session (AsyncSession): The database session.

    Returns:
        SampleResponseModel: The requested sample.
    """
    sample = await SampleService(session).get_sample(sample_id)
    return sample

@samples_router.post("/", status_code=HTTPStatus.CREATED)
async def create_sample(
    sample_create_data: SampleCreateModel, 
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Creates a new sample record. Requires authentication.

    Args:
        sample_create_data (SampleCreateModel): The data for the new sample.
        session (AsyncSession): The database session.
        current_user (dict): The authenticated user making the request.

    Returns:
        SampleResponseModel: The newly created sample.
    """
    new_sample = await SampleService(session).create_sample(sample_create_data)

    return new_sample

# Modify for cases where the id is: not found / incorrect length (37 characters)
# Modify to update the update attribute 
@samples_router.put("/{sample_id}", status_code=HTTPStatus.OK)
async def update_sample(
    sample_id: str,
    update_data: SampleCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Updates an existing sample record. Requires authentication.

    Args:
        sample_id (str): The UUID of the sample to update.
        update_data (SampleCreateModel): The new data for the sample.
        session (AsyncSession): The database session.
        current_user (dict): The authenticated user making the request.

    Returns:
        SampleResponseModel: The updated sample.
    """
    updated_sample = await SampleService(session).update_sample(sample_id, update_data)

    return updated_sample

@samples_router.delete("/{sample_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_sample(
    sample_id: str, 
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_active_user)
    ):
    """
    Deletes a sample record by its unique identifier. Requires authentication.

    Args:
        sample_id (str): The UUID of the sample to delete.
        session (AsyncSession): The database session.
        current_user (dict): The authenticated user making the request.

    Returns:
        dict: An empty dictionary indicating successful deletion.
    """
    await SampleService(session).delete_sample(sample_id)
    return {}