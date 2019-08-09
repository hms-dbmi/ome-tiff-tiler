#!/usr/bin/env bash
set -o errexit
set -o pipefail

start() { echo travis_fold':'start:$1; echo $1; }
end() { set +v; echo travis_fold':'end:$1; echo; echo; }
die() { set +v; echo "$*" 1>&2 ; exit 1; }

NAME=ome-tiff-tiler

start build
docker build --tag=$NAME context
end build

start run
# `realpath` is better, but not installed by default on travis.
INPUT=`pwd`/fixtures/test.ome.tif
OUTPUT=`pwd`/fixtures/output
rm -rf "$OUTPUT"
mkdir "$OUTPUT"
docker run \
    --rm \
    -e "CHANNEL_PAGE_PAIRS=polyT:0 nuclei:1" \
    -e "PREFIX=test_prefix" \
    --mount "type=bind,src=$INPUT,dst=/input.ome.tif" \
    --mount "type=bind,src=$OUTPUT,dst=/output_dir" \
    "$NAME"
end run

start compare
diff -w -r fixtures/output fixtures/output-expected/ -x .DS_Store \
  | head -n100 | cut -c 1-100
end compare

echo 'PASS!'
