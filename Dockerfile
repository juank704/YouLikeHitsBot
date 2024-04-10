FROM python:3.9

# Instalar dependencias para Chrome
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Configurar el entorno de trabajo
WORKDIR /YouLikeHitsBot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=/YouLikeHitsBot

# Comando para ejecutar al iniciar el contenedor
CMD ["python", "-u", "main.py"]
