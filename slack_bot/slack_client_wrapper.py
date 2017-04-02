import logging


class SlackClientWrapper:
    def __init__(self, slack_lib):
        self.slack_lib = slack_lib
        self.logger = logging.getLogger('SlackClientWrapper')

    def post_message(self, channel, message, as_user):
        self.slack_lib.api_call('chat.postMessage', channel=channel,
                                text=message, as_user=as_user)

    def get_users(self):
        self.logger.info('Getting users...')
        api_call = self.slack_lib.api_call('users.list')
        if api_call.get('ok'):
            return api_call.get('members')
        else:
            self.logger.error('The error %s was raised while '
                              'getting users!' % api_call.get('error'))
            return []

    def connect(self):
        return self.slack_lib.rtm_connect()

    def read(self):
        return self.slack_lib.rtm_read()
