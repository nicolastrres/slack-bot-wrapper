
class SlackClient:
    def __init__(self, slack_lib):
        self.slack_lib = slack_lib

    def post_message(self, channel, message, as_user):
        self.slack_lib.api_call('chat.postMessage', channel=channel,
                                text=message, as_user=as_user)

    def get_users(self):
        api_call = self.slack_lib.api_call('users.list')
        return api_call.get('members') if api_call.get('ok') else []


class SlackBot:
    def __init__(self, bot_name, client):
        self.client = client
        self.bot_name = bot_name

    def _get_users(self):
        api_call = self.client.api_call('users.list')
        return api_call.get('members') if api_call.get('ok') else []

    @property
    def id(self):
        for user in self._get_users():
            return user.get('id') if user.get('name') == self.bot_name else None
