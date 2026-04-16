# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Comando para correr la aplicación (incluye carga de datos iniciales)
CMD ["sh", "-c", "python src/load_initial_data.py && uvicorn src:app --host 0.0.0.0 --port 8000"]
