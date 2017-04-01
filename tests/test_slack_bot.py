import unittest
from unittest.mock import Mock

from slack_bot.slack_bot import SlackBot


class SlackBotTest(unittest.TestCase):
    def test_get_bot_id_successfully(self):
        users = [
            {'id': 'some-id', 'name': 'bot-name'},
            {'id': 'another-id', 'name': 'another-name'}
        ]
        api_call_response = {'ok': True, 'members': users}
        slack_client_mocked = Mock()
        slack_client_mocked.api_call.return_value = api_call_response

        slack_bot = SlackBot('bot-name', slack_client_mocked)

        self.assertEqual(slack_bot.id, 'some-id')

    def test_get_bot_id_wrong_name(self):
        users = [
            {'id': 'some-id', 'name': 'bot-name'},
            {'id': 'another-id', 'name': 'another-name'}
        ]
        api_call_response = {'ok': True, 'members': users}
        slack_client_mocked = Mock()
        slack_client_mocked.api_call.return_value = api_call_response

        slack_bot = SlackBot('wrong-bot-name', slack_client_mocked)

        self.assertIsNone(slack_bot.id)
