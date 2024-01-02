from moviepy.editor import *
import numpy as np
import os
import cv2
from PIL import Image, ImageDraw, ImageFont

# Path to BeReal Font
FONT_PATH = rf"static{os.path.sep}fonts{os.path.sep}Inter-Bold.ttf"
# Your BeReal Username
BEREAL_USERNAME = "kyleasaff"
# Duration of the Video
BEREAL_VIDEO_DURATION = 45
# Cap the speed of a frame at specified MIN_FRAME_DURATION (0.18 = 0.18s)
USE_MIN_FRAME_DURATION = True
MIN_FRAME_DURATION = 0.18


def bezier_curve(t, p0, p1, p2, p3):
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )


def add_splash_to_frame(
    frame,
    text,
    font_size,
    frame_width,
    frame_height,
    font_path=os.getcwd()
    + os.path.sep
    + "static"
    + os.path.sep
    + "fonts"
    + os.path.sep
    + "Inter-Bold.ttf",
    position=(0, 0),
    text_color=(0, 0, 255),
    logo=False
):

    # Convert OpenCV frame to Pillow Image
    img_pil = Image.fromarray(cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2RGB))

    # Create a draw object
    draw = ImageDraw.Draw(img_pil)

    # Specify font and size
    font = ImageFont.truetype(font_path, font_size)

    # Get text size
    text_size = draw.textbbox((0, 0), text, font=font)

    # Calculate the center of the frame with respect to text size
    center_x = int((frame_width - text_size[2]) / 2) + position[0]
    center_y = int((frame_height - text_size[3]) / 2) + position[1]

    # Add text to the image
    draw.text((center_x, center_y), text, font=font, fill=text_color)

    # Convert Pillow Image back to OpenCV frame
    frame_with_text = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    return frame_with_text



def add_text_to_frame(
    frame,
    text,
    font_size,
    frame_width,
    frame_height,
    font_path=os.getcwd()
    + os.path.sep
    + "static"
    + os.path.sep
    + "fonts"
    + os.path.sep
    + "tusker-grotesk-6700-bold.ttf",
    position=(0, 0),
    text_color=(0, 0, 255),
    logo=False
):

    # Convert OpenCV frame to Pillow Image
    img_pil = Image.fromarray(cv2.cvtColor(np.uint8(frame), cv2.COLOR_BGR2RGB))

    # Create a draw object
    draw = ImageDraw.Draw(img_pil)

    # Specify font and size
    font = ImageFont.truetype(font_path, font_size)

    # Get text size
    text_size = draw.textbbox((0, 0), text, font=font)

    # Calculate the center of the frame with respect to text size
    center_x = int((frame_width - text_size[2]) / 2) + position[0]
    center_y = int((frame_height - text_size[3]) / 2) + position[1]

    # Add text to the image
    draw.text((center_x, center_y), text, font=font, fill=text_color)

    if logo:
        bereal_font = ImageFont.truetype(FONT_PATH, 50)
        draw.text((center_x+215, center_y+842), "BeReal.", font=bereal_font, fill=(255, 255, 255))

    # Convert Pillow Image back to OpenCV frame
    frame_with_text = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    return frame_with_text


def generate_video(image_folder, output_path, frames_per_second, t_duration):
    images = sorted(
        [
            os.path.join(image_folder, img)
            for img in os.listdir(image_folder)
            if img.endswith(".webp")
        ]
    )

    # Generate the duration for each image based on bezier curve
    durations = []
    for i in range(len(images)):
        t = i / len(images)
        bc = bezier_curve(t, 2.0, 0.4, 0.3, 0.9)
        # print(bc)
        durations.append(bc)
    total_duration = np.sum(durations)
    normalized_durations = [
        duration * (t_duration / total_duration) for duration in durations
    ]
    print("Generating part1")
    part1 = ImageSequenceClip(images, durations=[2 / len(images)] * len(images))
    part1.write_videofile("part1.mp4", fps=frames_per_second)

    cap = cv2.VideoCapture("part1.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        "output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = add_text_to_frame(
                frame,
                "2023",
                200,
                width,
                height - 205,
                text_color=(255, 255, 255),
            )
            frame = add_text_to_frame(
                frame,
                "RECAP",
                200,
                width,
                height + 205,
                text_color=(255, 255, 255),
            )
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    # frame with black background
    blank = np.zeros((height, width, 3), np.uint8)
    blank = add_text_to_frame(
        blank,
        "2023",
        200,
        width,
        height - 205,
        text_color=(255, 255, 255),
    )
    blank = add_text_to_frame(
        blank,
        "RECAP",
        200,
        width,
        height + 205,
        text_color=(255, 255, 255),
        logo=True
    )
    for _ in range(75):
        out.write(blank)

    cap.release()
    out.release()
    print("Generating part2")

    # slow down the last 15 frames
    end_duration = normalized_durations[:15]
    end_duration.reverse()
    del normalized_durations[-15:]
    new_normalized_durations = normalized_durations + end_duration
    new_normalized_durations[-1] = new_normalized_durations[-1]

    print(new_normalized_durations)

    if USE_MIN_FRAME_DURATION:
        new_normalized_durations = [MIN_FRAME_DURATION if ele < MIN_FRAME_DURATION else ele for ele in new_normalized_durations]

    part2 = ImageSequenceClip(images, durations=new_normalized_durations)

    # generate part 3
    cap = cv2.VideoCapture("part1.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        "splash.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    # frame with black background
    blank = np.zeros((height, width, 3), np.uint8)
    blank = add_splash_to_frame(
        blank,
        "BeReal.",
        200,
        width,
        height,
        text_color=(255, 255, 255),
    )
    blank = add_splash_to_frame(
        blank,
        "BeRe.al/" + BEREAL_USERNAME,
        50,
        width,
        height + 280,
        text_color=(255, 255, 255),
    )
    for _ in range(75):
        out.write(blank)

    cap.release()
    out.release()


    # combine part1 and part2
    clips = [VideoFileClip("output.mp4"), part2, VideoFileClip("splash.mp4")]
    final_clip = concatenate_videoclips(clips, method="chain")
    final_clip.write_videofile(
        output_path, fps=frames_per_second, threads=6, codec="libx264"
    )
    # delete part1
    os.remove("part1.mp4")
    # delete output.mp4
    os.remove("output.mp4")
    # delete splash.mp4
    os.remove("splash.mp4")


def butidRecap():
    image_folder = os.path.join(os.getcwd(), "combined")
    output_path = (
        os.getcwd() + os.path.sep + "static" + os.path.sep + "slideshow_test.mp4"
    )
    frames_per_second = 30
    total_duration = BEREAL_VIDEO_DURATION

    generate_video(image_folder, output_path, frames_per_second, total_duration)
