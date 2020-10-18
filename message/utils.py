from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError
from datetime import datetime
from phone_iso3166.country import phone_country
from country_currencies import get_by_country
import logging
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)


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


def validate_recipients(recipient):
    validate_phone = ValidatePhoneNumber()
    valid_nos = []
    if isinstance(recipient, list):
        for number in recipient:
            if validate_phone(number):
                valid_nos.append(validate_phone(number))
        return valid_nos


def get_currency(recipient):
    log_prefix = "GET COUNTRY CODE FROM PHONE NUMBER"
    try:
        logger.info(u"{} {}".format(log_prefix, recipient))
        country_code = phone_country(recipient)
        logger.info(u"{} {}".format(log_prefix, country_code))
        currency = "".join(get_by_country(country_code))
        return currency
    except Exception as ex:
        logger.exception(u"{} {}".format(log_prefix, str(ex)))
        raise Exception(ex)
