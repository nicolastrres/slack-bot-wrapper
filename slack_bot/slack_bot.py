
class SlackBot:
    def __init__(self, bot_name, client, commands_handlers=None):
        self.client = client
        self.bot_name = bot_name
        self.commands_handlers = commands_handlers or {}

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
            return user.get('id') if user.get(
                'name') == self.bot_name else None

    @property
    def at_bot(self):
        return '<@' + self.id + '>'

    def handle_command(self, command, channel):
        if command in self.commands:
            self.commands_handlers[command]()
        else:
            self._unknown_command(channel)
