from message.models import Gateway, Message
from message.utils import ValidatePhoneNumber
import logging
import africastalking

logger = logging.getLogger(__name__)


def validate_recipients(recipient):
    validate_phone = ValidatePhoneNumber()
    valid_nos = []
    if isinstance(recipient, list):
        for number in recipient:
            if validate_phone(number):
                valid_nos.append(validate_phone(number))
        return valid_nos


def topup_airtime_via_at(recipient, amount, account_name=None, *args):
    log_prefix = "SEND AIRTIME VIA AT"
    if len(validate_recipients(recipient)) != 0:
        recipient = validate_recipients(recipient)
        recipient = ",".join(recipient)
        try:
            if account_name:
                gateway = Gateway.objects.get(
                    name="Africastalking", account_number=account_name, active=True
                )
            else:
                gateway = Gateway.objects.get(name="Africastalking", active=True)
        except Gateway.DoesNotExist as ex:
            raise Exception("Gateway is not set up for recipient {}".format(recipient))
        except Gateway.MultipleObjectsReturned:
            raise Exception("Multiple Gateway found for {}".format(recipient))
        else:
            africastalking.initialize(gateway.account_number, gateway.password)
            airtime = africastalking.Airtime
            kwargs = {
                "phone_number": recipient,
                "amount": amount,
                "currency_code": "KES",
            }

            response = send_topup(airtime, **kwargs)
            logger.info("{}-{}".format(log_prefix, response))
            if response["responses"]:
                if response["responses"][0]["status"] == "Sent":
                    parse_and_save_response(
                        response
                    )  # make it a celery task recommended
                return response
    else:
        return


def parse_and_save_response(response):
    log_prefix = "PARSE AND SAVE RESPONSE"
    logging.info("{} {}".format(log_prefix, response))
    try:
        message_id = response["responses"][0]["requestId"]
        recipients = response["responses"][0]["phoneNumber"]
        status = response["responses"][0]["status"]
        if status == "Sent":
            status_code = 201

        gateway = Gateway.objects.get(name="Africastalking")
        message = Message(
            gateway=gateway,
            status_code=status_code,
            recipient=recipients,
            status=status,
            partner_message_id=message_id,
        )
        message.append_comment("DLR", response)
        message.save()
    except KeyError as ex:
        logger.exception("{} {} {}".format(log_prefix, "Missing Key", ex))


def send_topup(airtime, **kwargs):
    response = airtime.send(**kwargs)
    return response
