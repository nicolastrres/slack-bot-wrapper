import unittest
from unittest.mock import Mock
from slack_bot import SlackClientWrapper


class SlackClientWrapperTest(unittest.TestCase):
    def setUp(self):
        self.slack_lib_mocked = Mock()
        self.slack_client = Mock()
        self.slack_lib_mocked.return_value = self.slack_client

    def test_post_message(self):
        slack_wrapper = SlackClientWrapper(
            slack_lib=self.slack_lib_mocked,
            slack_token=123
        )
        channel = 'some-channel'
        message = 'some-text'
        as_user = True
        slack_wrapper.post_message(
            channel=channel,
            message=message,
            as_user=as_user
        )

        self.slack_client.api_call.assert_called_once_with(
            'chat.postMessage',
            channel=channel,
            text=message,
            as_user=as_user
        )

    def test_get_user(self):
        slack_wrapper = SlackClientWrapper(
            slack_lib=self.slack_lib_mocked,
            slack_token=123
        )
        slack_wrapper.get_users()

        self.slack_client.api_call.assert_called_once_with('users.list')

    def test_connect(self):
        slack_wrapper = SlackClientWrapper(
            slack_lib=self.slack_lib_mocked,
            slack_token=123
        )
        slack_wrapper.connect()

        self.assertTrue(self.slack_client.rtm_connect.called)
