# Use the official Python image as a base
FROM mcr.microsoft.com/azure-functions/python:4-python3.10-slim

# NEW: Install prerequisites for adding new package repositories
RUN apt-get update && apt-get install -y curl gnupg

# NEW: Add Microsoft package repository for ODBC driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# NEW: Install the ODBC driver and accept the EULA
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Set the working directory in the container
WORKDIR /home/site/wwwroot

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port that the Azure Function Host will run on
EXPOSE 80