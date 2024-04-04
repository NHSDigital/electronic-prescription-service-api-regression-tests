import random
import string

# Prescription ID check digits use a modified version of the ISO 7064, MOD 37-2 algorithm with "+" substituted for "*".
CHECK_DIGIT_VALUES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+"


def generate_short_form_id_from_existing(original_short_form_id: str) -> str:
    prescriber_ods_code = original_short_form_id[7:13]
    return generate_short_form_id(prescriber_ods_code)


def generate_short_form_id(prescriber_ods_code: str) -> str:
    a = generate_random_hex_string(6)
    b = prescriber_ods_code.zfill(6)
    c = generate_random_hex_string(5)
    check_digit = calculate_check_digit(a + b + c)
    return f"{a}-{b}-{c}{check_digit}"


def validate_short_form_id(input_: str) -> bool:
    input_without_delimiters = input_.replace("-", "")
    input_without_check_digit = input_without_delimiters[:-1]
    check_digit = input_without_delimiters[-1]
    return validate_check_digit(input_without_check_digit, check_digit)


def generate_random_hex_string(length: int) -> str:
    return "".join(random.choices(string.hexdigits[:-6], k=length)).upper()


def calculate_check_digit(input_: str) -> str:
    total = calculate_total_for_check_digit(input_)
    check_digit_index = (38 - total) % 37
    return CHECK_DIGIT_VALUES[check_digit_index]


def validate_check_digit(input_: str, check_digit: str) -> bool:
    total = calculate_total_for_check_digit(input_)
    check_digit_value = CHECK_DIGIT_VALUES.index(check_digit)
    return (total + check_digit_value) % 37 == 1


def calculate_total_for_check_digit(input_: str) -> int:
    return sum(int(charStr, 36) for charStr in input_) % 37


if __name__ == "__main__":
    # Example usage:
    ods_code = "A99968"
    generated_id = generate_short_form_id(ods_code)
    new_generated_id = generate_short_form_id_from_existing(generated_id)
    # print("Original Short Form ID:", generated_id)
    # print("Is Valid:", validate_short_form_id(generated_id))
    # print("New Short Form ID:", new_generated_id)
    # print("Is Valid:", validate_short_form_id(new_generated_id))
    print(
        "prescription ID from TypeScript script valid??? ",
        str(validate_short_form_id("DAF875-A99968-443DAC")),
    )
