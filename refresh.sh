#!/bin/sh

python soft/downloader.py --force
python soft/move.py
python soft/normalizer.py