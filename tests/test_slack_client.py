import unittest
from unittest.mock import Mock
from slack_bot import SlackClientWrapper


class SlackClientTest(unittest.TestCase):
    def setUp(self):
        self.slack_lib_mocked = Mock()

    def test_post_message(self):
        slack_client = SlackClientWrapper(self.slack_lib_mocked)
        channel = 'some-channel'
        message = 'some-text'
        as_user = True
        slack_client.post_message(
            channel=channel,
            message=message,
            as_user=as_user
        )

        self.slack_lib_mocked.api_call.assert_called_once_with(
            'chat.postMessage',
            channel=channel,
            text=message,
            as_user=as_user
        )

    def test_get_user(self):
        slack_client = SlackClientWrapper(self.slack_lib_mocked)
        slack_client.get_users()

        self.slack_lib_mocked.api_call.assert_called_once_with('users.list')

    def test_connect(self):
        slack_client = SlackClientWrapper(self.slack_lib_mocked)
        slack_client.connect()

        self.assertTrue(self.slack_lib_mocked.rtm_connect.called)