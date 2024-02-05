from PIL import Image, ImageDraw
import os


def add_logo_left(logo_path: str, image: Image, height: int, banner_height: int, left: int, padding: int) -> int:
    draw_height = banner_height - padding * 2
    logo = Image.open(logo_path).convert('RGBA')
    new_width = (logo.width * draw_height) // logo.height
    logo = logo.resize((new_width, draw_height))
    image.paste(logo, (left + padding, height - logo.height - padding))
    return left + logo.width + padding


def add_logo_right(logo_path: str, image: Image, height: int, banner_height: int, right: int, padding: int) -> int:
    draw_height = banner_height - padding * 2
    logo = Image.open(logo_path).convert('RGBA')
    new_width = (logo.width * draw_height) // logo.height
    logo = logo.resize((new_width, draw_height))
    image.paste(logo, (right - logo.width - padding * 2, height - logo.height - padding))
    return right - logo.width - padding * 2


def add_bottom_banner(image_path, output_folder):
    # Open the image
    image = Image.open(image_path)

    width, height = image.size
    ratio = width / height if width > height else height / width
    banner_height = int(height * 0.12 / ratio)
    padding = int(banner_height * 0.1)
    left = 0
    logos = ['logo/rupp.png', 'logo/sca.png', 'logo/fe.png']
    for logo in logos:
        left = add_logo_left(logo, image, height, banner_height, left, padding)
    image = add_background(image, banner_height, left, padding)
    left = 0
    for logo in logos:
        left = add_logo_left(logo, image, height, banner_height, left, padding)
    right = width
    qrs = []
    if width / height < 1:
        qrs = ['logo/facebook-label.png']
    elif width / height < 1.2:
        qrs = ['logo/telegram-label.png', 'logo/facebook-label.png']
    else:
        qrs = ['logo/website-label.png', 'logo/telegram-label.png', 'logo/facebook-label.png']
    for qr in qrs:
        right = add_logo_right(qr, image, height, banner_height, right, padding)
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    image.save(output_path)


def add_background(image: Image, banner_height: int, left: int, padding: int) -> Image:
    bg = Image.new("RGBA", (image.width, banner_height), (21, 55, 83))
    draw = ImageDraw.Draw(bg)
    bg_color = (255, 255, 255)
    draw.polygon([(0, 0), (left, 0), (left + banner_height, banner_height), (0, banner_height)], fill=bg_color)
    start_x = left + padding * 2
    start_y = padding * 2
    points = [
        (start_x, start_y),
        (start_x + padding * 1.5, start_y),
        (start_x + banner_height - padding, banner_height - padding * 0.5),
        (image.width, banner_height - padding * 0.5),
        (image.width, banner_height),
        (start_x + banner_height - padding, banner_height),
        (start_x + padding * 1.5, start_y + padding * 0.5),
        (start_x + padding * 0.5, start_y + padding * 0.5),
    ]
    draw.polygon(points, fill='white')

    start_x = left + padding
    start_y = padding * 0.5
    points = [
        (start_x, start_y),
        (start_x + padding, start_y),
        (start_x + padding * 2, start_y + padding),
        (start_x + padding, start_y + padding),
    ]
    draw.polygon(points, fill=(221, 71, 63))
    image.paste(bg, (0, image.height - banner_height))
    return image

path = '/Users/stone-wh/Library/CloudStorage/OneDrive-RoyalUniversityofPhnomPenh/01 - ASCSE/Student - Seminar & Events/07 - NGS Visit (31Jan2024)'
input_folder = f'{path}/Original'
output_folder = f'{path}/Banner'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        print(f"Processing {filename}...")
        image_path = os.path.join(input_folder, filename)
        add_bottom_banner(image_path, output_folder)

print("Process completed.")
