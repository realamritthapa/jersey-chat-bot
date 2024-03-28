# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="amrit@pdx.edu"

# Execute apt-get update and install to get Python's package manager
#  installed (pip)
RUN apt-get update -y
RUN apt-get install -y python3-pip

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

ENV PORT 8080
ENV HOST 0.0.0.0
# Install the Python packages specified by requirements.txt into the container
RUN pip install -r requirements.txt

# Set the program that is invoked upon container instantiation
ENTRYPOINT ["python3"]

# Set the parameters to the program
CMD ["app.py"]