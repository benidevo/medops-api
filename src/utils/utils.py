import random
from uuid import uuid4


def generate_temp_id():
    return str(uuid4())


def generate_otp():
    return str(random.randint(100000, 999999))


def replace_space(file_name):
    return file_name.replace(" ", "_")
