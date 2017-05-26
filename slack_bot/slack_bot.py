import logging

import time


class SlackBot:
    def __init__(self, bot_name, client, commands_handlers=None):
        self.client = client
        self.bot_name = bot_name
        self.commands_handlers = commands_handlers or {}
        self.logger = logging.getLogger('SlackBot')

    def _unknown_command(self, channel):
        commands = ', '.join(self.commands)

        response = 'Not sure what you mean. ' \
                   'Available commands are: %s' % commands
        self.client.post_message(
            channel=channel,
            message=response,
            as_user=True
        )

    @property
    def commands(self):
        return sorted([command for command in self.commands_handlers.keys()])

    @property
    def id(self):
        for user in self.client.get_users():
            if user.get('name') == self.bot_name:
                return user.get('id')
        return None

    @property
    def at_bot(self):
        return '<@' + self.id + '>'

    def handle_command(self, command_received, channel):
        command_found = False
        for existent_command in self.commands:
            if command_received.startswith(existent_command):
                command_found = True
                self.commands_handlers[existent_command]()
        if not command_found:
            self._unknown_command(channel)

    def _text_in_output(self, output):
        return output['text'].split(self.at_bot)[1].strip().lower()

    @staticmethod
    def _channel_in_output(output):
        return output['channel']

    def _parse_output(self, output_list):
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.at_bot \
                        in output['text']:
                    return self._text_in_output(output), \
                           self._channel_in_output(output)

        return None, None

    def start(self):
        READ_WEBSOCKET_DELAY = 1
        if self.client.connect():
            self.logger.info('Connected and running!')
            while True:
                command, channel = self._parse_output(self.client.read())
                if command and channel:
                    self.handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            self.logger.error("Connection failed. Invalid Slack token?")
