import random
from uuid import uuid4


def generate_temp_id():
    return str(uuid4())


def generate_otp():
    return str(random.randint(100000, 999999))


def replace_space(file_name):
    return file_name.replace(" ", "_")


def minutes_to_seconds(minutes):
    return minutes * 60


def hours_to_seconds(hours):
    return minutes_to_seconds(hours * 60)


def days_to_seconds(days):
    return hours_to_seconds(days * 24)
