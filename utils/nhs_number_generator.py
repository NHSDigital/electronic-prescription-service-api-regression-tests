"""Generate 10-digit NHS numbers
"""

from __future__ import unicode_literals

from random import choice, randint

check_digit_weights = {0: 10, 1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2}
ranges = ((500000000, 599999999), (900000000, 999999999))


def calculate_check_digit(nhs_number):
    """Given the first 9 or 10 digits of a 10-digit NHS number, calculate the check digit.

    Returns:
        int: The check digit.
             Note that this function may return 10, in which case the NHS number is invalid.

    """

    # The procedure for calculating the check digit, according to:
    # https://www.datadictionary.nhs.uk/data_dictionary/attributes/n/nhs/nhs_number_de.asp

    # Step 1) Multiply each of the first nine digits by a weighting factor
    products = [int(nhs_number[i]) * check_digit_weights[i] for i in range(9)]

    # Step 2) Add the results of each multiplication together.
    sum_products = sum(products)

    # Step 3) Divide the total by 11 and establish the remainder.
    remainder = sum_products % 11

    # Step 4) Subtract the remainder from 11 to give the check digit.
    eleven_minus_remainder = 11 - remainder

    # If the result is 11 then a check digit of 0 is used.
    if eleven_minus_remainder == 11:
        return 0

    # If the result is 10 then the NHS number is invalid.
    return eleven_minus_remainder


def random_nhs_number_generator():
    """Returns a generator for an unpredictable sequence of 10-digit NHS numbers.

    The default ranges are the ones currently issued in England, Wales and the Isle of Man.
    Numbers outside of this range may be valid but could conflict with identifiers used in
    Northern Ireland and Scotland. See https://en.wikipedia.org/wiki/NHS_number

    Args:
        ranges [(int, int), ...]: Specify the ranges for the sequence.
          You must exclude the check digits.

    """
    for _range in ranges:
        if _range[1] < _range[0]:
            raise ValueError(
                "The high end of the range should not be lower than the low end."
            )

        if (_range[1] - _range[0]) == 0:
            only_possible_check_digit = calculate_check_digit(
                "{:09d}".format(_range[0])
            )
            if only_possible_check_digit == 10:
                raise ValueError("{:09d} is not a valid NHS number.".format(_range[0]))

    while True:
        # Pick a tuple (a, b) at random from ranges and get a random int >= a and <= b.
        # Note that this weights the ranges equally, no matter their size
        candidate_number = "{:09d}".format(randint(*choice(ranges)))
        check_digit = calculate_check_digit(candidate_number)

        if check_digit != 10:
            nhs_number = candidate_number + str(check_digit)
            print(f"NHS Number: {nhs_number}")
            return nhs_number


def is_valid_nhs_number(nhs_number):
    """Checks whether the NHS number is valid.

    NHS numbers in 3-3-4 format should be converted first, i.e. with remove_separators().

    """
    if (
        (not isinstance(nhs_number, str) and not isinstance(nhs_number, type("")))
        or len(nhs_number) != 10
        or not nhs_number.isnumeric()
    ):
        return False

    check_digit = calculate_check_digit(nhs_number)

    # The check digit shouldn't be 10 (how could it be, it is only one digit)
    if check_digit == 10:
        return False

    return str(check_digit) == nhs_number[9]


if __name__ == "__main__":
    print(random_nhs_number_generator())
