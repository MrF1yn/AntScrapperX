# Use the official Python 3.12 image as the base
FROM selenium/standalone-chrome:latest

## Set environment variables
ENV PYTHONUNBUFFERED=1
##    DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
#RUN apt-get update && apt-get install -y \
#    wget \
#    curl \
#    gnupg \
#    unzip \
#    && rm -rf /var/lib/apt/lists/*

## Install Google Chrome
#RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
#    apt-get update && apt-get install -y \
#    google-chrome-stable && \
#    rm -rf /var/lib/apt/lists/*
#
## Install ChromeDriver
#RUN wget -N https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.110/linux64/chromedriver-linux64.zip && \
#    unzip chromedriver-linux64.zip && \
#    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
#    chmod +x /usr/local/bin/chromedriver && \
#    rm -rf chromedriver-linux64 chromedriver-linux64.zip
#
## Set the working directory
WORKDIR /app
RUN sudo chmod -R 777 /app
RUN mkdir -p /tmp/chrome-data && \
    chmod -R 777 /tmp/chrome-data
RUN sudo apt update -y
RUN sudo apt install python3.12-venv -y
COPY EnvDriverBot.py /app/
COPY Driver.py /app/
COPY AmazonScrapper.py /app/
COPY FlipkartScrapper.py /app/
COPY QuoraScrapper.py /app/
COPY CombinedScrapper.py /app/
COPY AmazonScrapper.py /app/
COPY MicrosoftNumber.py /app/
COPY Dependencies.py /app/
COPY Runner.py /app/
COPY requirements.txt /app/
# Copy the script and requirements into the container

RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

#COPY requirements.txt /app/

# Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt
# Define the default command to run the script
CMD ["python", "Runner.py"]