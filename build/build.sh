#!/bin/sh
set -e

mkdir -p "${PREFIX}/bin"
mkdir -p "${PREFIX}/database"
cp -r bin/* "${PREFIX}/bin/"
cp -r database/* "${PREFIX}/database/"

