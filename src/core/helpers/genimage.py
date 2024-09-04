from os.path import dirname, join

from PIL import Image, ImageDraw, ImageFont
from prisma.models import Booking


WIDTH = 1080
HEIGHT = 1920
BORDER_HEIGHT = 150


ASSETS_DIRECTORY = join(dirname(__file__), "../../../", "assets")
IMAGE_PATH = join(ASSETS_DIRECTORY, "images/digiscreen_bg.png")
FONT_PATH = join(ASSETS_DIRECTORY, "fonts/inter.ttf")


def generate_common_image(
    common_name: str, primary_color: str, secondary_color: str, bookings: list[Booking]
):
    img = Image.open(IMAGE_PATH)
    draw = ImageDraw.Draw(img)

    # Top and bottom borders
    draw.rectangle(((0, 0), (WIDTH, BORDER_HEIGHT)), fill=primary_color)
    draw.rectangle(((0, HEIGHT - BORDER_HEIGHT), (WIDTH, HEIGHT)), fill=primary_color)

    # Common Name
    font = ImageFont.truetype(FONT_PATH, size=100)

    common_fontsize = 100
    title_space_start = 150
    title_space_end = 600

    common_name_space = title_space_end - title_space_start
    text_size = draw.textlength(common_name, font=font)

    # Calculate centered position
    x = (WIDTH - text_size) / 2
    y = 130 + (common_name_space - common_fontsize) / 2

    # Draw the common name
    draw.text((x, y), common_name, font=font, fill=primary_color)

    table_margin = 16
    table_cell_height = 80
    # x locations, and width of each of the table columns
    table_header_sizes = [(16, 320), (352, 400), (768, 296)]

    title_y_start = title_space_end
    table_titles = ["CLASSES", "LOCATION", "TEACHER"]
    for title, (start, width) in zip(table_titles, table_header_sizes):
        draw_centered_text_in_rectangle(
            draw, start, title_y_start, width, table_cell_height, title, secondary_color
        )

    row_start = title_y_start + table_cell_height + table_margin
    for booking in bookings:
        if booking.course is None or booking.teacher is None or booking.space is None:
            continue

        columns = [booking.course.code, booking.space.name, booking.teacher.code]
        for text, (start, width) in zip(columns, table_header_sizes):
            draw_centered_text_in_rectangle(
                draw, start, row_start, width, table_cell_height, text
            )

        row_start += table_cell_height + table_margin

    return img


def draw_centered_text_in_rectangle(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    width: int,
    height: int,
    text: str,
    fill: str | None = None,
    text_color: str = "black",
    stroke: str = "black",
):
    font_size = 24
    font = ImageFont.truetype(FONT_PATH, font_size)

    text_width, text_height = draw.textlength(text, font=font), font_size

    # Calculate position to center the text
    text_x = x + (width - text_width) / 2
    text_y = y + (height - text_height) / 2 - 3

    roundness = 10
    draw.rounded_rectangle(
        [x, y, x + width, y + height], roundness, fill=fill, outline=stroke, width=3
    )

    draw.text((text_x, text_y), text, font=font, fill=text_color)
