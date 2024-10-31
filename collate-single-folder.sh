#!/bin/bash

# List of subdirectories to exclude
exclude_dirs=("$@")

# Define the target directories for symbolic links
train_target="./training-set-single"

# Remove target directories
rm -rf "$train_target"
# Create target directories if they don't exist
mkdir -p "$train_target/labels" "$train_target/images"

# Deal with the config
cp ./training-set/data.yaml ./training-set-single/data.yaml
# Get the absolute path of the main folder
abs_path=$(realpath "$train_target")
# Replace stuff
sed -i "s|training-set/|$abs_path/|g" ./training-set-single/data.yaml


# Function to check if a directory is in the exclude list
is_excluded() {
    local dir="$1"
    for exclude in "${exclude_dirs[@]}"; do
        if [[ "$dir" == *"$exclude"* ]]; then
            return 0
        fi
    done
    return 1
}

# Iterate over each subdirectory in data
for folder in data/*; do
    if is_excluded "$folder"; then
        echo "Excluding $folder"
        continue
    fi

    # Create symbolic links for train, valid, and test subfolders if they exist
    for subset in train valid test; do
        if [[ -d "$folder/$subset/images" ]]; then
            ln -s $PWD/$folder/$subset/images/* $PWD/$train_target/images/
            echo "Linked $folder/$subset/images to $PWD/$train_target/images/"
            for file in "${folder}/${subset}/images"/*; do
            	echo "./images/$(basename "$file")" >> "$train_target/$subset.txt"
           	done
        fi

        if [[ -d "$folder/$subset/labels" ]]; then
            ln -s $PWD/$folder/$subset/labels/*.txt $PWD/$train_target/labels/
            echo "Linked $folder/$subset/labels to $PWD/$train_target/labels/"
        fi
    done
done