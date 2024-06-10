import uuid

CHECK_DIGIT_VALUES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+"


def generate_short_form_id(ods_code=None, original_short_form_id=None) -> str:
    if original_short_form_id is None and ods_code is None:
        raise ValueError("An original prescription id or ODS code must be provided")
    hex_string = str(uuid.uuid4()).replace("-", "").upper()
    first = hex_string[:6]
    middle = (
        original_short_form_id[7:13]
        if original_short_form_id
        else ods_code.zfill(6)  # pyright: ignore [reportOptionalMemberAccess]
    )
    last = hex_string[12:17]
    prescription_id = f"{first}-{middle}-{last}"
    prescription_id = generate_check_digit(prescription_id)
    print("Generated prescription id:", prescription_id)
    return prescription_id


def generate_check_digit(prescription_id):
    formatted_prescription_id = prescription_id.replace("-", "")
    prescription_id_length = len(formatted_prescription_id)
    running_total = 0
    for index, character in enumerate(formatted_prescription_id):
        running_total += int(character, 36) * 2 ** (prescription_id_length - index)
    check_value = (38 - (running_total % 37)) % 37
    check_digit = CHECK_DIGIT_VALUES[check_value]
    prescription_id += check_digit
    return prescription_id


# Example usage:
if __name__ == "__main__":
    generated_prescription_id = generate_short_form_id(
        ods_code="X26", original_short_form_id=None
    )
    print(generated_prescription_id)
