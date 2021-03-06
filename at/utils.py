from message.models import Gateway
from message.response import AfricaStalkingResponse
import logging
import africastalking
from message.utils import validate_recipients, get_currency

logger = logging.getLogger(__name__)


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
                "currency_code": get_currency(recipient),
            }

            response = send_topup(airtime, **kwargs)
            logger.info("{}-{}".format(log_prefix, response))
            at_response = AfricaStalkingResponse(recipient, response)
            at_response.handle_response()
            return response
    else:
        return


def send_topup(airtime, **kwargs):
    response = airtime.send(**kwargs)
    return response
