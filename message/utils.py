from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

import logging


class ValidatePhoneNumber:
    def __call__(self, phone_number):
        if phone_number:
            phone_number = str(phone_number).strip()
        if not phone_number.startswith("+"):
            phone_number = "+" + phone_number
        try:
            validate_international_phonenumber(phone_number)
        except ValidationError as error:
            logging.exception("{}-{}".format("VALIDATE PHONENUMBER", str(error)))
        else:
            return phone_number


def format_comment(existing_comment, prefix, new_comment):
    if existing_comment:
        f_comment = u"{} {} [{}] {}".format(existing_comment, now, prefix, new_comment)
        return f_comment
    else:
        f_comment = u"{} {} [{}] {}".format(existing_comment, now, prefix, new_comment)
        return f_comment
