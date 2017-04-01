
class SlackClient:
    def __init__(self, slack_lib):
        self.slack_lib = slack_lib

    def post_message(self, channel, message, as_user):
        self.slack_lib.api_call('chat.postMessage', channel=channel,
                                text=message, as_user=as_user)

    def get_users(self):
        api_call = self.slack_lib.api_call('users.list')
        return api_call.get('members') if api_call.get('ok') else []
