#!/bin/bash

# List of subdirectories to exclude
exclude_dirs=("$@")

# Define the target directories for symbolic links
train_target="./training-set/train"
valid_target="./training-set/valid"
test_target="./training-set/test"

# Remove target directories
rm -rf "$train_target" "$valid_target" "$test_target"
# Create target directories if they don't exist
mkdir -p "$train_target" "$valid_target" "$test_target"

# Add images and labels
for subset in train valid test; do
	mkdir -p "$PWD/training-set/$subset/images" "$PWD/training-set/$subset/labels";
done

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
        target=$subset
        if [[ "$subset" == "test" ]]; then
            target="train"
        fi
        if [[ -d "$folder/$subset/images" ]]; then
            ln -s $PWD/$folder/$subset/images/* $PWD/training-set/$target/images/
            echo "Linked $folder/$subset/images to $PWD/training-set/$target/images/"
        fi

        if [[ -d "$folder/$subset/labels" ]]; then
            ln -s $PWD/$folder/$subset/labels/*.txt $PWD/training-set/$target/labels/
            echo "Linked $folder/$subset/labels to $PWD/training-set/$target/labels/"
        fi
    done
done
