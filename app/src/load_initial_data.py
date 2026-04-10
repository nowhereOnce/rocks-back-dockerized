import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import csv
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session, init_db
from src.samples.schemas import SampleCreateModel
from src.samples.service import SampleService

async def create_initial_data():
    async with get_session() as session:
        sample_service = SampleService(session)

        with open('src/datos_rocas.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sample_data = SampleCreateModel(
                    rock_name=row['Roca'],
                    description=row['Descripción'] if 'Descripción' in row else "",
                    location_name=row['Localidad'],
                    location_country=row['País'],
                    cut=row['Corte'].lower() == 'sí',
                    thin_section=row['Lámina delgada'].lower() == 'sí' if row['Lámina delgada'] else False,
                    picture=row['Foto']
                )
                await sample_service.create_sample(sample_data)

if __name__ == "__main__":
    asyncio.run(create_initial_data())