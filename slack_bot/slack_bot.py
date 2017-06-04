import logging

import time


class SlackBot:
    def __init__(self, bot_name, client, commands_handlers=None):
        self.client = client
        self.bot_name = bot_name
        self.commands_handlers = commands_handlers or {}
        self.logger = logging.getLogger('[%sbot]' % self.bot_name)

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
        """
        List of commands available
        :return: Commands
        :type: list of str
        """
        return sorted([command for command in self.commands_handlers.keys()])

    @property
    def id(self):
        """
        Slack Bot ID
        :return: Bot id
        :type: str
        """
        for user in self.client.get_users():
            if user.get('name') == self.bot_name:
                return user.get('id')
        return None

    @property
    def at_bot(self):
        """
        At bot <@bot_id>
        :return: @bot_id
        :type: str
        """
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

    def _parse_events(self, events_list):
        if events_list:
            for event in events_list:
                if 'text' in event and self.at_bot in event['text']:
                    return self._text_in_output(event), \
                           self._channel_in_output(event)

    def start(self):
        """
        Start bot and connect it with slack
        :return: None
        """
        if self.client.connect():
            self.logger.info('Connected and running!')
            self._keep_bot_reading()
        else:
            self.logger.error("Connection failed. Invalid Slack token?")

    def _keep_bot_reading(self):
        read_websocket_delay = 1
        while True:
            command, channel = self._parse_events(self.client.read())
            if command and channel:
                self.handle_command(command, channel)
            time.sleep(read_websocket_delay)
