#use Python slim-bullseye base image
FROM python:3.9-slim-bullseye

#set working directory
WORKDIR /app

#copy application code and requirements file
COPY requirements.txt /app/requirements.txt
COPY . /app

#install minimal system dependencies and upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    && pip install --no-cache-dir --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

#install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#install minimal Playwright dependencies for Firefox
RUN pip install --no-cache-dir playwright \
    && playwright install-deps firefox \
    && playwright install firefox

#remove unnecessary files
RUN apt-get remove --purge -y \
    curl \
    wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc /usr/share/man

#expose the application port
EXPOSE 5004

#set the container entry point
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=5004", "--server.address=0.0.0.0"]

