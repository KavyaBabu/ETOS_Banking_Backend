import phonenumbers
import re
import os


def get_host(request):
    return request.META.get('HTTP_HOST', "")


def validate_uk_mobile_number(number) -> bool:
    """
    Validates a UK mobile number.

    Args:
        number (str): The mobile number to validate.

    Returns:
        bool: Whether the number is valid or not.
    """
    try:
        parsed_number = phonenumbers.parse(number, 'GB')
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.search(pattern, email):
        return True
    return False


def validate_mobile_number(value):
    pattern = r"\d{10}"

    if re.search(pattern, value):
        return True
    else:
        return False
