from nhs_number_generator.generate_nhs_numbers import random_nhs_number_generator


def generate_multiple(
    nhs_number_range=(
        (311300000, 319999999),
        (400000000, 499999999),
        (600000000, 799999999),
    ),
    amount_to_generate=1,
):
    numbers = [
        next(random_nhs_number_generator(nhs_number_range))
        for _ in range(amount_to_generate)
    ]
    # Keep only one of each
    unique_numbers = set(numbers)
    return unique_numbers


def generate_single(
    nhs_number_range=(
        (311300000, 319999999),
        (400000000, 499999999),
        (600000000, 799999999),
    )
):
    numbers = [next(random_nhs_number_generator(nhs_number_range)) for _ in range(1)]
    # Keep only one of each
    unique_numbers = set(numbers).pop()
    print("NHS Number: ", unique_numbers)
    return unique_numbers


if __name__ == "__main__":
    num_to_generate = 10
    for nhs_number in generate_multiple(amount_to_generate=num_to_generate):
        print(nhs_number)
