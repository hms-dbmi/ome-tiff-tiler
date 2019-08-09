# OME-TIFF Tiler

Builds [ome-tiff-tiler](https://hub.docker.com/r/gehlenborglab/ome-tiff-tiler) Docker image:
This image uses [libvips](https://jcupitt.github.io/libvips/) to convert
[OME-TIFF](https://docs.openmicroscopy.org/ome-model/6.0.1/ome-tiff/) files to
[DeepZoom](https://en.wikipedia.org/wiki/Deep_Zoom) tiles for each image plane.

## Build

```bash
docker build --tag=ome-tiff-tiler context
```

## Run

```bash
docker run \
    -rm \
    -e "CHANNEL_PAGE_PAIRS=channel0:0 channel1:1" \
    -e "PREFIX=your_prefix" \
    --mount "type=bind,src=YOUR_FILE.tif,dst=/input.ome.tif" \
    --mount "type=bind,src=YOUR_OUTPUT,dst=/output_dir" \
    ome-tiff-tiler
```
(Or `gehlenborglab/ome-tiff-tiler:latest` to pull from DockerHub.)

Two environment variables should be set:
- `CHANNEL_PAGE_PAIRS`: Space-delimited pairs of layer name and corresponding TIFF index.
- `PREFIX`: Prefix to prepend to tile filenames.

And two mounts should be provided:
- Replace `YOUR_FILE.tif` with absolute path of the OME-TIFF to tile.
- Replace `YOUR_OUTPUT` with absolute path of directory where the tiles should go.

## Test and push to DockerHub

```bash
./test.sh
```

If tests pass, we're just pushing to DockerHub by hand:
```bash
# First, set VERSION.
docker tag ome-tiff-tiler gehlenborglab/ome-tiff-tiler:$VERSION
docker push gehlenborglab/ome-tiff-tiler:$VERSION
