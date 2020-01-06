#!/usr/bin/env python3
import pyvips
import argparse
import os


def tile_ometiff(filename, channel_pages, output_directory, prefix):
    for (channel, page) in channel_pages:
        image = pyvips.Image.tiffload(filename, page=page)

        path = os.path.join(
            output_directory,
            '{}.images.{}'.format(prefix, channel)
        )

        if not os.path.exists(path):
            os.mkdir(path)

        pyvips.Image.dzsave(image, os.path.join(path, channel), overlap=0, tile_size=256)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create tiles with DeepZoom file.')
    parser.add_argument(
        '--ometiff_file',
        help='OME-TIFF image to be tiled.')
    parser.add_argument(
        '--channel_page_pairs', required=True, nargs='+',
        help='Colon-delimited pairs of channels and page values')
    parser.add_argument(
        '--output_directory', required=True,
        help='Directory for output')
    parser.add_argument(
        '--prefix', required=True,
        help='Prefix for tile filenames')
    args = parser.parse_args()

    channel_pages = [pair.split(':') for pair in args.channel_page_pairs]

    tile_ometiff(
        filename=args.ometiff_file,
        channel_pages=channel_pages,
        output_directory=args.output_directory,
        prefix=args.prefix
    )
