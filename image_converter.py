import os

from PIL import Image


def cr2_to_jpg(input_path):
    """Converts a CR2 image to a JPG image."""
    # Open the CR2 image file
    with Image.open(input_path) as img:
        # Save the image as a JPG file
        output_path = input_path.replace(".cr2", ".JPG")
        img.save(output_path, "JPEG")
    os.remove(input_path)


def image_converter(input_folder):
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.cr3'):
            print(f"Processing {filename}...")
            image_path = os.path.join(input_folder, filename)
            cr2_to_jpg(image_path)
    print("Process completed.")
