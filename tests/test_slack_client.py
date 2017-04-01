import unittest
from unittest.mock import Mock

from slack_bot.slack_client import SlackClient


class SlackClientTest(unittest.TestCase):
    def setUp(self):
        self.slack_lib = Mock()

    def test_post_message(self):
        slack_client = SlackClient(self.slack_lib)
        channel = 'some-channel'
        message = 'some-text'
        as_user = True
        slack_client.post_message(
            channel=channel,
            message=message,
            as_user=as_user
        )

        self.slack_lib.api_call.assert_called_once_with(
            'chat.postMessage',
            channel=channel,
            text=message,
            as_user=as_user
        )

    def test_get_user(self):
        slack_client = SlackClient(self.slack_lib)
        slack_client.get_users()

        self.slack_lib.api_call.assert_called_once_with('users.list')
