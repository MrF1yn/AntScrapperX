# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the AmazonScrapper.py script to the working directory
COPY AmazonScrapper.py .

# Set the command to run the AmazonScrapper.py script
CMD ["python", "AmazonScrapper.py"]