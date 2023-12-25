from PIL import Image, ImageDraw, ImageFont, ImageChops
import os

def overlay_images(primary_folder, secondary_folder, output_folder):

    font_size = 50
    offset = 50
    text_opacity=150

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through primary folder
    for primary_filename in os.listdir(primary_folder):
        # Extract prefix from primary filename
        primary_prefix = primary_filename.split('_')[0]
        date = primary_prefix

        # Check if there's a corresponding file in the secondary folder with the same prefix
        secondary_files = [file for file in os.listdir(secondary_folder) if file.startswith(primary_prefix)]
        if secondary_files:
            # Use the first matching file in the secondary folder
            secondary_filename = secondary_files[0]

            primary_path = os.path.join(primary_folder, primary_filename)
            secondary_path = os.path.join(secondary_folder, secondary_filename)

            # Load primary and secondary images
            # TO DO: Could be possible to pull these images directly from the API Endpoint, that way we won't have to use a database in the future
            primary_image = Image.open(primary_path)
            secondary_image = Image.open(secondary_path)
            source = Image.open(os.path.join(os.getcwd(), "static\images\secondary_image_outline.png"))

            primary_image = primary_image.convert("RGBA")
            secondary_image = secondary_image.convert("RGBA")
            source = source.convert("RGBA")

            #create border around secondary image
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
            # Choose a font (you may need to provide the path to a font file)static\fonts\Inter-SemiBold.ttf
            font = ImageFont.truetype(r'static\fonts\Inter-Bold.ttf', font_size)
            # Get the bounding box of the text
            text_bbox = draw.textbbox((0, 0), date, font=font)
            # Calculate the position to center the text
            x = (width - text_bbox[2]) // 2
            y = (height - text_bbox[3]) - offset

            # Calculate the size of the rectangle to fill the text_bbox
            rect_width = text_bbox[2] + 20  # Add some padding
            rect_height = text_bbox[3] + 20  # Add some padding

            # Draw a semi-transparent filled rectangle as the background
            
            # TO DO: So I just kinda eyeballed these offsets to make it fit, im too lazy to figure out the right ones automatically 
            #        To get picture perfect accuracy.
            draw.rectangle([(x - 30, y - 15), (x + rect_width + 10, y + rect_height + 10)], fill=(0, 0, 0, text_opacity))

            # Draw the text on the image
            draw.text((x, y), date, font=font, fill="white")
            # Save the modified image

            # Save the result in the output folder
            output_path = os.path.join(output_folder, f'combined_{primary_filename}')
            primary_image.save(output_path)

            print(f"Combined image saved at: {output_path}")

def create_images():
    # Example usage
    primary_folder = os.path.join(os.getcwd(), 'primary')
    secondary_folder = os.path.join(os.getcwd(), 'secondary')
    output_folder = os.path.join(os.getcwd(), 'combined')
    
    overlay_images(primary_folder, secondary_folder, output_folder)
