#!/usr/bin/env python3
import pyvips
import argparse
from pathlib import Path
from urllib.parse import urljoin
import re
import json
import xmltodict
from enum import Enum


class PyramidType(Enum):
    tiff = 'tiff'
    dz = 'dz'

    def __str__(self):
        return self.value


def tile_dz(filename, channel_pages, output_directory, prefix):
    for (channel, page) in channel_pages:
        image = pyvips.Image.tiffload(filename, page=page)
        path = Path(output_directory, "{}.images.{}".format(prefix, channel))
        path.mkdir(exist_ok=True)
        pyvips.Image.dzsave(image, str(Path(path, channel)), overlap=0, tile_size=256)


def tile_tiff(filename, output_directory, prefix, server_url):
    tile_size = 512
    image = pyvips.Image.tiffload(filename)
    metadata_str = image.get("image-description")
    namespaces = {
        "http://www.openmicroscopy.org/Schemas/OME/2016-06": None,
        "http://www.openmicroscopy.org/Schemas/SA/2016-06": None,
    }
    output_metadata = {}
    image_metadata = xmltodict.parse(
        metadata_str, process_namespaces=True, namespaces=namespaces
    )["OME"]["Image"]["Pixels"]
    channel_metadata = image_metadata["Channel"]
    output_metadata = {}
    output_subdirectory = f"{prefix}.images"
    path = Path(output_directory, output_subdirectory)
    print(f"Writing images to {path}")
    for channel in channel_metadata:
        # Channel1:0 - this appears to be an error in vanderbilt's metadata
        output_metadata[channel["@Name"]] = {}
    for i, channel in enumerate(output_metadata):
        Path(path).mkdir(exist_ok=True)
        image = pyvips.Image.tiffload(filename, page=i)
        image.tiffsave(
            str(Path(path, f"{channel}.ome.tiff")),
            strip=True,
            tile=True,
            tile_width=tile_size,
            tile_height=tile_size,
            pyramid=True,
            compression="VIPS_FOREIGN_TIFF_COMPRESSION_DEFLATE",
        )
        output_metadata[channel]["tileSource"] = urljoin(
            server_url, str(Path(output_subdirectory, f"{channel}.ome.tiff"))
        )
        output_metadata[channel]["sample"] = 1
    tiff_json_path = str(Path(path, "tiff.json"))
    print(f"Writing metadata to {tiff_json_path}")
    with open(tiff_json_path, "w") as outfile:
        json.dump(output_metadata, outfile, indent=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create tiles for DeepZoom or TIFF pyramids.'
    )
    parser.add_argument(
        '--pyramid_type',
        help='Which kind of pyramid to use',
        type=PyramidType,
        choices=list(PyramidType),
        required=True,
    )
    parser.add_argument('--ometiff_file', help='OME-TIFF image to be tiled.')
    parser.add_argument(
        '--channel_page_pairs',
        nargs="*",
        help='Colon-delimited pairs of channels and page values',
        default='',
    )
    parser.add_argument(
        '--output_directory', required=True, help='Directory for output'
    )
    parser.add_argument('--prefix', required=True, help='Prefix for tile filenames')
    parser.add_argument(
        '--server_url', nargs="?", help='Where the files will be served from',
    )
    args = parser.parse_args()

    if args.pyramid_type == PyramidType.dz:
        channel_pages = [pair.split(':') for pair in args.channel_page_pairs]
        tile_dz(
            filename=args.ometiff_file,
            channel_pages=channel_pages,
            output_directory=args.output_directory,
            prefix=args.prefix,
        )
    elif args.pyramid_type == PyramidType.tiff:
        tile_tiff(
            filename=args.ometiff_file,
            output_directory=args.output_directory,
            prefix=args.prefix,
            server_url=args.server_url,
        )
