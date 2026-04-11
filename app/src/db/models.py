from sqlmodel import SQLModel, Field,Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List

#Table Models

class User(SQLModel, table=True):
    """
    Represents a user in the system.
    
    Attributes:
        uid (UUID): Primary key, uniquely identifies the user.
        username (str): Unique username for authentication.
        email (str): Unique email address.
        first_name (str): User's first name.
        last_name (str): User's last name.
        is_active (bool): Whether the user account is active.
        hashed_password (str): The salted and hashed password.
        created_at (datetime): Timestamp of record creation.
        updated_at (datetime): Timestamp of last record update.
    """
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    is_active: bool = Field(default=True)
    hashed_password: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

class Rocks(SQLModel, table=True):
    """
    Represents a type of rock in the database.
    
    Attributes:
        uid (UUID): Primary key, uniquely identifies the rock type.
        name (str): The name of the rock.
        description (str | None): A brief description of the rock.
        created_at (datetime): Timestamp of record creation.
        updated_at (datetime): Timestamp of last record update.
        samples (List[Samples]): List of samples associated with this rock type.
    """
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    # Relationship with Samples
    samples: List["Samples"] = Relationship(back_populates="rock")


class Locations(SQLModel, table=True):
    """
    Represents a geographic location where samples are found.
    
    Attributes:
        uid (UUID): Primary key, uniquely identifies the location.
        name (str): The name of the location (e.g., city, region).
        country (str): The country where the location is situated.
        created_at (datetime): Timestamp of record creation.
        updated_at (datetime): Timestamp of last record update.
        samples (List[Samples]): List of samples collected from this location.
    """
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    country: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    # Relationship with Samples
    samples: List["Samples"] = Relationship(back_populates="location")

class Samples(SQLModel, table=True):
    """
    Represents a specific physical sample collected.
    
    Attributes:
        uid (UUID): Primary key, uniquely identifies the sample.
        rock_uid (UUID): Foreign key referencing the associated rock type.
        location_uid (UUID): Foreign key referencing the collection location.
        cut (bool): Indicates if the sample has been cut.
        thin_section (bool): Indicates if a thin section has been prepared.
        picture (str): URL or path to a photograph of the sample.
        created_at (datetime): Timestamp of record creation.
        updated_at (datetime): Timestamp of last record update.
        rock (Optional[Rocks]): The associated rock type object.
        location (Optional[Locations]): The associated location object.
    """
    uid: UUID = Field(default_factory=uuid4, primary_key=True)
    rock_uid: UUID = Field(default=None, foreign_key="rocks.uid")
    location_uid: UUID = Field(default=None, foreign_key="locations.uid")
    cut: bool
    thin_section: bool
    picture: str #subject to change
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    # Relationship with Rocks
    rock: Optional[Rocks] = Relationship(back_populates="samples")

    # Relationship with Locations
    location: Optional[Locations] = Relationship(back_populates="samples")
