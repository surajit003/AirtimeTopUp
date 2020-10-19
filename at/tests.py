from django.test import TestCase
from mock import Mock
import at.utils
from message.models import Gateway, Message
from message.response import AfricaStalkingResponse


class SMSTaskTests(TestCase):
    def setUp(self) -> None:
        self.gateway = Gateway.objects.create(
            name="Africastalking",
            account_number="828299292",
            api_url="https://test.url",
            password="jkjfjdjkfjkdfjf",
            configured_sender="993939393",
            active=True,
        )
        self.at_valid_response = {'errorMessage': 'None', 'numSent': 1, 'totalAmount': 'KES 100.0000',
                                  'totalDiscount': 'KES 4.0000', 'responses': [
                {'phoneNumber': '+254771621379', 'errorMessage': 'None', 'amount': 'KES 100.0000', 'status': 'Sent',
                 'requestId': 'ATQid_5389c866eb760cba818893cb8f068c93', 'discount': 'KES 4.0000'}]}
        self.at_error_response = {'errorMessage': 'A duplicate request was received within the last 5 minutes', 'numSent': 0, 'totalAmount': '0', 'totalDiscount': '0', 'responses': []}
        self.recipient = '9999999'

    def test_top_up_airtime_via_at(self):
        at.utils.topup_airtime_via_at = Mock(return_value='mock_response')
        self.assertEqual(at.utils.topup_airtime_via_at(), 'mock_response')

    def test_handle_response_with_valid_payload(self):
        at_response_handler = AfricaStalkingResponse(self.recipient, self.at_valid_response)
        at_response_handler.handle_response()
        message = Message.objects.get(partner_message_id=self.at_valid_response['responses'][0]['requestId'])
        self.assertIsNotNone(message)
        self.assertEqual(message.partner_message_id, self.at_valid_response['responses'][0]['requestId'])

    def test_handle_response_with_error_payload(self):
        at_response_handler = AfricaStalkingResponse(self.recipient, self.at_error_response)
        message = at_response_handler.handle_response()
        self.assertIsNotNone(message)
    def test_handle_response_with_missing_key(self):
        at_response_handler = AfricaStalkingResponse(self.recipient, '')
        with self.assertRaises(Exception):
            at_response_handler.handle_response()



