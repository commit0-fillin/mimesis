"""This module provides internal util functions."""

def luhn_checksum(num: str) -> str:
    """Calculate a checksum for num using the Luhn algorithm.

    Used to validate credit card numbers, IMEI numbers,
    and other identification numbers.

    :param num: The number to calculate a checksum for as a string.
    :return: Checksum for number.
    """
    digits = [int(d) for d in num if d.isdigit()]
    
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    total = sum(digits)
    checksum = (10 - (total % 10)) % 10
    
    return str(checksum)
