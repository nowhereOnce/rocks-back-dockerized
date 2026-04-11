import sys
import os
import asyncio
import csv

# Add the parent directory of 'src' to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from src.db.main import AsyncSessionLocal, init_db
from src.db.models import User, Samples
from src.auth import get_password_hash
from src.config import settings
from src.samples.schemas import SampleCreateModel
from src.samples.service import SampleService

async def create_admin_user(session):
    statement = select(User).where(User.username == settings.ADMIN_USERNAME)
    result = await session.exec(statement)
    admin_user = result.first()

    if not admin_user:
        print(f"Creating default admin user: {settings.ADMIN_USERNAME}")
        new_admin = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            first_name="Admin",
            last_name="User",
            is_active=True
        )
        session.add(new_admin)
        await session.commit()
    else:
        print(f"Admin user '{settings.ADMIN_USERNAME}' already exists.")

async def create_initial_data():
    await init_db()
    async with AsyncSessionLocal() as session:
        # Create admin user
        await create_admin_user(session)

        # Create samples from CSV only if no samples exist
        sample_service = SampleService(session)
        
        # Check if samples already exist
        existing_samples_statement = select(Samples)
        existing_samples_result = await session.exec(existing_samples_statement)
        if existing_samples_result.first():
            print("Samples already exist in the database. Skipping sample creation.")
        else:
            csv_path = os.path.join(os.path.dirname(__file__), 'datos_rocas.csv')
            if not os.path.exists(csv_path):
                print(f"CSV file not found at {csv_path}")
            else:
                with open(csv_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        sample_data = SampleCreateModel(
                            rock_name=row['Roca'],
                            description=row['Descripción'] if 'Descripción' in row else "",
                            location_name=row['Localidad'],
                            location_country=row['País'],
                            cut=row['Corte'].lower() == 'sí',
                            thin_section=row['Lámina delgada'].lower() == 'sí' if row.get('Lámina delgada') else False,
                            picture=row['Foto']
                        )
                        await sample_service.create_sample(sample_data)
                print("Initial samples loaded successfully.")

if __name__ == "__main__":
    asyncio.run(create_initial_data())