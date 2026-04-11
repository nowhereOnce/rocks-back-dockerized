from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Locations
from .schemas import LocationCreateModel
from sqlmodel import select


class LocationService:
    """
    Service class for managing location-related database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the LocationService with a database session.

        Args:
            session (AsyncSession): The asynchronous database session.
        """
        self.session = session

    async def get_all_locations(self):
        """
        Retrieves all locations from the database, ordered by creation date.

        Returns:
            List[Locations]: A list of location objects.
        """
        statement = select(Locations).order_by(Locations.created_at)
        result = await self.session.exec(statement)
        return result.all()

    async def create_location(self, location_create_data: LocationCreateModel):
        """
        Creates and persists a new location in the database.

        Args:
            location_create_data (LocationCreateModel): Data for the new location.

        Returns:
            Locations: The newly created and persisted location object.
        """
        new_location = Locations(**location_create_data.model_dump())
        self.session.add(new_location)
        await self.session.commit()
        return new_location

    async def get_location(self, location_uid: str):
        """
        Retrieves a single location by its unique identifier.

        Args:
            location_uid (str): The UUID of the location.

        Returns:
            Optional[Locations]: The location object if found, otherwise None.
        """
        statement = select(Locations).where(Locations.uid == location_uid)
        result = await self.session.exec(statement)
        return result.first()

    async def update_location(self, location_uid: str, location_update_data: LocationCreateModel):
        """
        Updates an existing location's information.

        Args:
            location_uid (str): The UUID of the location to update.
            location_update_data (LocationCreateModel): The updated data.

        Returns:
            Optional[Locations]: The updated location object.
        """

        statement = select(Locations).where(Locations.uid == location_uid)
        result = await self.session.exec(statement)
        location = result.first()
        for key, value in location_update_data.model_dump().items():
            setattr(location, key, value)
        await self.session.commit()
        return location

    async def delete_location(self, location_uid: str):
        """
        Removes a location from the database.

        Args:
            location_uid (str): The UUID of the location to delete.
        """
        statement = select(Locations).where(Locations.uid == location_uid)
        result = await self.session.exec(statement)
        location = result.first()
        await self.session.delete(location)
        await self.session.commit()
