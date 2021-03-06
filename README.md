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

Example:

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

Environment variables should be set:

- `CHANNEL_PAGE_PAIRS`: (Only for use with `dz` pyramid type) Space-delimited pairs of layer name and corresponding TIFF index.
- `PREFIX`: Prefix to prepend to tile filenames.
- `SERVER_URL`: (Only for use with `tiff` pyramid type) For creating metadata that can be used as a JSON, put in the protocol, host, and any (other) prefix of the server_url
- `PYRAMID_TYPE`: One of `dz` and `tiff` for either Deepzoom (channel clamped) or TIFF pyramid
  And two mounts should be provided:
- Replace `YOUR_FILE.tif` with absolute path of the OME-TIFF to tile.
- Replace `YOUR_OUTPUT` with absolute path of directory where the tiles should go.

## Test and push to DockerHub

```bash
./test.sh
```

If tests pass, we're just pushing to DockerHub by hand:

```bash
# We should only push from master:
git checkout master
git pull

# First, set the new VERSION:
VERSION=v0.0.????
# If need be, build the image
docker build --tag=ome-tiff-tiler context
docker tag ome-tiff-tiler gehlenborglab/ome-tiff-tiler:$VERSION
docker push gehlenborglab/ome-tiff-tiler:$VERSION

# And also make a git tag:
git tag $VERSION
git push origin $VERSION
```
