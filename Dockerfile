# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Install libvips and pyvips
RUN apt-get update
RUN apt-get install libvips -y
RUN pip install pyvips==2.1.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD python ometiff_tiler.py \
    --ometiff_file /input.ome.tif \
    --channel_page_pairs $CHANNEL_PAGE_PAIRS \
    --output_directory /output_dir \
    --dataset_name $DATASET_NAME \
