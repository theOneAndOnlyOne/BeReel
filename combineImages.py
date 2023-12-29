from multiprocessing import Pool
import multiprocessing
from PIL import Image, ImageDraw, ImageFont, ImageChops
import os

OUTLINE_PATH = f"static{os.path.sep}images{os.path.sep}secondary_image_outline.png"
FONT_PATH = rf"static{os.path.sep}fonts{os.path.sep}Inter-Bold.ttf"


def process_image(primary_filename, primary_folder, secondary_folder, output_folder):
    font_size = 50
    offset = 50
    text_opacity = 150

    # Extract prefix from primary filename
    primary_prefix = primary_filename.split("_")[0]
    date = primary_prefix

    # Check if there's a corresponding file in the secondary folder with the same prefix
    secondary_files = [
        file for file in os.listdir(secondary_folder) if file.startswith(primary_prefix)
    ]
    if secondary_files:
        # Use the first matching file in the secondary folder
        secondary_filename = secondary_files[0]

        primary_path = os.path.join(primary_folder, primary_filename)
        secondary_path = os.path.join(secondary_folder, secondary_filename)

        # Load primary and secondary images and ignore if image cant be opened

        try:
            primary_image = Image.open(primary_path)
            secondary_image = Image.open(secondary_path)
        except:
            print(f"Could not open image: {primary_path}, skipping...")
            return
        source = Image.open(os.path.join(os.getcwd(), OUTLINE_PATH))

        primary_image = primary_image.convert("RGBA")
        secondary_image = secondary_image.convert("RGBA")
        source = source.convert("RGBA")

        # Create border around secondary image
        secondary_image = ImageChops.multiply(source, secondary_image)

        # Resize secondary image to fraction the size of the primary image
        width, height = primary_image.size
        new_size = (width // 3, height // 3)
        secondary_image = secondary_image.resize(new_size)

        # Overlay secondary image on top-left corner of primary image
        primary_image.paste(secondary_image, (10, 10), secondary_image)

        # Get the image dimensions
        width, height = primary_image.size
        # Create a drawing object
        draw = ImageDraw.Draw(primary_image)
        # Choose a font (you may need to provide the path to a font file)
        font = ImageFont.truetype(FONT_PATH, font_size)
        # Get the bounding box of the text
        text_bbox = draw.textbbox((0, 0), date, font=font)
        # Calculate the position to center the text
        x = (width - text_bbox[2]) // 2
        y = (height - text_bbox[3]) - offset

        # Calculate the size of the rectangle to fill the text_bbox
        rect_width = text_bbox[2] + 20  # Add some padding
        rect_height = text_bbox[3] + 20  # Add some padding

        # Draw a semi-transparent filled rectangle as the background
        draw.rectangle(
            [(x - 30, y - 15), (x + rect_width + 10, y + rect_height + 10)],
            fill=(0, 0, 0, text_opacity),
        )

        # Draw the text on the image
        draw.text((x, y), date, font=font, fill="white")
        # Save the modified image

        # Save the result in the output folder
        output_path = os.path.join(output_folder, f"combined_{primary_filename}")
        primary_image.save(output_path)

        print(f"Combined image saved at: {output_path}")


def overlay_images(primary_folder, secondary_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of primary filenames
    primary_filenames = os.listdir(primary_folder)

    # Use multiprocessing to process images in parallel
    pool = Pool(processes=multiprocessing.cpu_count() // 2)
    pool.starmap(
        process_image,
        [
            (primary_filename, primary_folder, secondary_folder, output_folder)
            for primary_filename in primary_filenames
        ],
    )


def create_images():
    # Example usage
    primary_folder = os.path.join(os.getcwd(), "primary")
    secondary_folder = os.path.join(os.getcwd(), "secondary")
    output_folder = os.path.join(os.getcwd(), "combined")

    overlay_images(primary_folder, secondary_folder, output_folder)
