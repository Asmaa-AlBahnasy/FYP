import os
import cv2
import numpy as np
from hashlib import md5
from PIL import Image
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def calculate_image_hash(image_path):
    """Calculate hash for an image."""
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        resized_image = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
        normalized_image = resized_image / 255.0
        diff = normalized_image > normalized_image.mean()
        hash_value = ''.join(['1' if v else '0' for v in diff.flatten()])
        return hash_value
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def remove_duplicates(folder_path):
    """Remove duplicate images from a folder."""
    if not os.path.isdir(folder_path):
        print(f"The path {folder_path} is not a valid directory.")
        return

    image_hashes = {}
    duplicate_count = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue  # Skip if not a file

        image_hash = calculate_image_hash(file_path)
        if image_hash is None:
            continue

        if image_hash in image_hashes:
            print(f"Duplicate found: {file_path} is a duplicate of {image_hashes[image_hash]}")
            os.remove(file_path)
            duplicate_count += 1
        else:
            image_hashes[image_hash] = file_path

    print(f"Removed {duplicate_count} duplicate images.")

# Specify the path to your folder
folder_path = "data"
remove_duplicates(folder_path)


#########################################################################################################################


# Function to resize images
def resize_images(input_folder, output_folder, size=(512, 512)):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Full path to the file
        input_path = os.path.join(input_folder, filename)

        # Skip if not an image
        if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')):
            continue

        try:
            # Open the image
            with Image.open(input_path) as img:
                # Resize the image while maintaining quality
                img = img.resize(size, Image.LANCZOS)  # LANCZOS filter for high-quality resizing

                # Output path
                output_path = os.path.join(output_folder, filename)

                # Save the image with maximum quality
                img.save(output_path, quality=95, optimize=True)
                print(f"Resized and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Plot the first resized image from the output folder
    plot_first_image(output_folder)

# Function to plot the first image from the output folder
def plot_first_image(output_folder):
    images = [f for f in os.listdir(output_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not images:
        print("No images to display.")
        return

    first_image_path = os.path.join(output_folder, images[0])
    try:
        with Image.open(first_image_path) as img:
            plt.imshow(img)
            plt.title(f"First Image: {images[0]}")
            plt.axis('off')
            plt.show()
    except Exception as e:
        print(f"Error displaying {images[0]}: {e}")

input_folder = "data"
output_folder = "LANCZOS_resized"

# Call the function to resize images
resize_images(input_folder, output_folder)



#########################################################################################################################




# Function to apply sharpening filter to images
def apply_sharpening_filter(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Full path to the file
        input_path = os.path.join(input_folder, filename)

        # Skip if not an image
        if not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png')):
            continue

        try:
            # Open the image
            with Image.open(input_path) as img:
                # Apply the sharpening filter
                sharpened_img = img.filter(ImageFilter.SHARPEN)

                # Output path
                output_path = os.path.join(output_folder, filename)

                # Save the sharpened image with maximum quality
                sharpened_img.save(output_path, quality=95, optimize=True)
                print(f"Sharpened and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Plot the first sharpened image from the output folder
    plot_first_image(output_folder)

# Function to plot the first image from the output folder
def plot_first_image(output_folder):
    images = [f for f in os.listdir(output_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not images:
        print("No images to display.")
        return

    first_image_path = os.path.join(output_folder, images[0])
    try:
        with Image.open(first_image_path) as img:
            plt.imshow(img)
            plt.title(f"First Image: {images[0]} (Sharpened)")
            plt.axis('off')
            plt.show()
    except Exception as e:
        print(f"Error displaying {images[0]}: {e}")

# Define your input and output folder paths
resized_folder = "LANCZOS_resized"
sharpened_output_folder = "SHARPENED_images"

# Call the function to apply sharpening filter
apply_sharpening_filter(resized_folder, sharpened_output_folder)
