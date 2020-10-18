from .models import Message, Gateway
import logging
import uuid

logger = logging.getLogger(__name__)


class AirtimeResponse:
    def __init__(self, phone_number, response):
        self.response = response
        self.phone_number = phone_number

    def handle_response(self):
        pass


class AfricaStalkingResponse(AirtimeResponse):
    def __save_response(self, **kwargs):
        log_prefix = "AT  RESPONSE"

        try:
            message_id = kwargs["requestId"]
            recipients = kwargs["phoneNumber"]
            status = kwargs["status"]
            status_code = kwargs["status_code"]
            gateway = Gateway.objects.get(name="Africastalking")
            message = Message(
                gateway=gateway,
                status_code=status_code,
                recipient=recipients,
                status=status,
                partner_message_id=message_id,
            )
            message.append_comment("DLR", self.response)
            message.save()
        except KeyError as ex:
            logger.exception("{} {} {}".format(log_prefix, "Missing Key", ex))
        return

    def handle_response(self):
        if (
            self.response["responses"]
            and self.response["responses"][0]["status"] == "Sent"
        ):
            message_id = self.response["responses"][0]["requestId"]
            recipients = self.response["responses"][0]["phoneNumber"]
            status = self.response["responses"][0]["status"]
            kwargs = {
                "requestId": message_id,
                "phoneNumber": recipients,
                "status": status,
                "status_code": 201,
            }
        else:
            # bad data
            message_id = "NOT-AT" + str(
                uuid.uuid4()
            )  # generate a non AT request Id to identify that it is created by us
            recipient = self.phone_number
            status = "FAIL"
            status_code = 200
            kwargs = {
                "requestId": message_id,
                "phoneNumber": recipient,
                "status": status,
                "status_code": status_code,
            }
        self.__save_response(**kwargs)
        return
