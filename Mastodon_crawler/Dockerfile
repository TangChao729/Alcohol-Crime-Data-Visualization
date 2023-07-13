# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8080

# Use environment variables for server, token and database
ENV SERVER_URL=""
ENV TOKEN="None"

ENV DATABASE_IP="None"
ENV DATABASE_PORT="None"
ENV DATABASE_USER="None"
ENV DATABASE_PASSWORD="None"
ENV DATABASE_NAME="None"


# Define the command to run the application
CMD python StartCrawling.py -server $SERVER_URL -token $TOKEN -c1 $DATABASE_IP -c2 $DATABASE_PORT -c3 $DATABASE_USER -c4 $DATABASE_PASSWORD -database $DATABASE_NAME

# Define the command to run the application
# CMD ["python", "StartCrawling.py", "-server", "https://mastodon.au", "-token", "NorMU8AqS0mWRFXX13BcJasmMXaHKEA_V8eHk_51lfE", "-database", "m3"]