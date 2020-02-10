FROM python:3.6-slim

# Always run `apt-get update` and `apt-get install` together.
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

RUN apt-get update && apt-get install -y \
  libvips
RUN pip install \
  pyvips==2.1.8 \
  xmltodict==0.12.0

COPY ometiff_tiler.py .

CMD python ometiff_tiler.py \
    --ometiff_file /input.ome.tif \
    --channel_page_pairs $CHANNEL_PAGE_PAIRS \
    --server_url $SERVER_URL \
    --pyramid_type $PYRAMID_TYPE \
    --output_directory /output_dir \
    --prefix $PREFIX
