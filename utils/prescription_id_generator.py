import random
import os


def get_new_prescription_id():
    random_bytes = os.urandom(6)
    hex_string = random_bytes.hex().upper()
    id_str = str(hex_string) + "A830082EFE3"
    id_str += calculate_check_digit(id_str)
    return f"{id_str[:6]}-{id_str[6:12]}-{id_str[12:22]}"


def calculate_check_digit(input_str):
    check_digit_values = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+"
    total = calculate_total_for_check_digit(input_str)
    check_digit_index = (38 - total) % 37
    return check_digit_values[check_digit_index]


def calculate_total_for_check_digit(input_str):
    return sum(int(char, 36) for char in input_str) * 2 % 37
