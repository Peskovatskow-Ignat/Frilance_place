from PIL import Image
from io import BytesIO
import secrets
import string
from random import random


def generate_secure_string(length=50):
    alphabet = string.ascii_letters
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secure_string


def resize_and_convert_to_jpg(image_data):
    image = Image.open(BytesIO(image_data))
    image = image.convert('RGB')
    image_resized = image.resize((1080, 1024))
    output_buffer = BytesIO()
    image_resized.save(output_buffer, format="JPEG")
    jpg_data = output_buffer.getvalue()

    return jpg_data


def profile_photo(image_data):
    image = Image.open(BytesIO(image_data))
    image = image.convert('RGB')
    image_resized = image.resize((75, 75))
    output_buffer = BytesIO()
    image_resized.save(output_buffer, format="JPEG")
    jpg_data = output_buffer.getvalue()

    return jpg_data
