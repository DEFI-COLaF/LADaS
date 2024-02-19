#!/bin/sh

mkdir -p training-set/test training-set/train training-set/valid
cp -r data/*/train/* ./training-set/train
cp -r data/*/valid/* ./training-set/valid
cp -r data/*/test/* ./training-set/test