# OME-TIFF Tiler

This is a Docker image to run ometiff_tiler.py using pyvips, a Python binding to the libvips command line tool. The tiler takes an OME-TIFF file and will create DeepZoom image tiles for each image plane.

## Run
```
docker build --tag=ometifftiler .
```
This will create a docker image with the tag ometifftiler.

```
docker run  
    -e "CHANNEL_PAGE_PAIRS=channel0:0 channel1:1"
    -e "DATASET_NAME=name"
    --mount "type=bind,src=/source.ome.tif=/input.ome.tif"
    --mount "type=bind,src=/destination,destination=/output_dir"
    --name tiler ometifftiler
```

This will create a container with the name tiler. Replace `channel0:0 channel1:1`, `name`, `source.ome.tif`, and `/destination` with your desired input.

`CHANNEL_PAGE_PAIRS`: expects the name of the image channel and its respective image page index in the source file separated with a colon as so "channel0:0".

`DATASET_NAME`: expects the name of the data set the image belongs to

`src` (with source.ome.tif): expects the OME-TIFF file you would like to tile.

`src` (with \destination): expects the directory you would like to store the DeepZoom tiles.
