import unittest
from functools import partial
from unittest.mock import Mock

from slack_bot import SlackBot


class SlackBotTest(unittest.TestCase):
    def setUp(self):
        self.users = [
            {'id': 'some-id', 'name': 'bot-name'},
            {'id': 'another-id', 'name': 'another-name'}
        ]
        self.slack_client_mocked = Mock()

    def test_get_bot_id_successfully(self):
        self.slack_client_mocked.get_users.return_value = self.users
        slack_bot = SlackBot('bot-name', self.slack_client_mocked)

        self.assertEqual(slack_bot.id, 'some-id')

    def test_get_bot_id_wrong_name(self):
        self.slack_client_mocked.get_users.return_value = self.users

        slack_bot = SlackBot('wrong-bot-name', self.slack_client_mocked)

        self.assertIsNone(slack_bot.id)

    def test_at_bot(self):
        self.slack_client_mocked.get_users.return_value = self.users

        slack_bot = SlackBot('bot-name', self.slack_client_mocked)

        self.assertEqual(slack_bot.at_bot, '<@some-id>')

    def test_handle_command_calling_right_handler(self):
        mocked_command = Mock()
        command_handlers = {
            'help': mocked_command,
            'another_command': Mock()
        }

        slack_bot = SlackBot(
            'bot-name',
            self.slack_client_mocked,
            commands_handlers=command_handlers
        )

        slack_bot.handle_command('help', 'some_channel')
        self.assertTrue(mocked_command.called)

    def test_handle_command_calling_right_handler_with_args(self):
        mocked_command = Mock()
        command_handlers = {
            'help': partial(mocked_command, 'some-arg'),
            'another_command': Mock()
        }

        slack_bot = SlackBot(
            'bot-name',
            self.slack_client_mocked,
            commands_handlers=command_handlers
        )

        slack_bot.handle_command('help', 'some_channel')
        mocked_command.assert_called_once_with('some-arg')

    def test_handle_command_show_available_commands_when_not_existent_command(
            self
    ):
        command_handlers = {
            'help': Mock(),
            'another_command': Mock()
        }
        expected_message = 'Not sure what you mean. ' \
                           'Available commands are: another_command, help'

        slack_bot = SlackBot(
            'bot-name',
            self.slack_client_mocked,
            commands_handlers=command_handlers
        )

        slack_bot.handle_command('not-existent-command', 'some-channel')
        self.slack_client_mocked.post_message.assert_called_once_with(
            channel='some-channel',
            message=expected_message,
            as_user=True
        )

    def test_get_sorted_commands(self):
        command_handlers = {
            'help': Mock(),
            'another_command': Mock()
        }

        slack_bot = SlackBot(
            'bot-name',
            self.slack_client_mocked,
            commands_handlers=command_handlers
        )
        self.assertEqual(slack_bot.commands, ['another_command', 'help'])

    def test_parse_event(self):
        self.slack_client_mocked.get_users.return_value = self.users
        event = [{
            'text': '<@some-id> something',
            'channel': 'some-channel'
        }]

        slack_bot = SlackBot(
            'bot-name',
            self.slack_client_mocked
        )

        actual_text, actual_channel = slack_bot._parse_events(event)

        self.assertEqual(actual_channel, 'some-channel')
        self.assertEqual(actual_text, 'something')
