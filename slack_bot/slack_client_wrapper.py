import logging

from slackclient import SlackClient


class SlackClientWrapper:
    def __init__(self, slack_token, slack_lib=SlackClient):
        self.slack_client = slack_lib(slack_token)
        self.logger = logging.getLogger('SlackClientWrapper')

    def post_message(self, channel, message, as_user):
        self.slack_client.api_call('chat.postMessage', channel=channel,
                                    text=message, as_user=as_user)

    def get_user(self, user_id):
        api_call = self.slack_client.api_call(
            'users.info',
            user=user_id
        )
        if api_call.get('ok'):
            return api_call.get('user')
        else:
            self.logger.error('The error %s was raised while '
                              'getting user information!' %
                              api_call.get('error'))

    def get_users(self):
        self.logger.info('Getting users...')
        api_call = self.slack_client.api_call('users.list')
        if api_call.get('ok'):
            return api_call.get('members')
        else:
            self.logger.error('The error %s was raised while '
                              'getting users!' % api_call.get('error'))
            return []

    def get_channel_users(self, channel_name):
        self.logger.info('Getting users of channel %s...' % channel_name)
        api_call = self.slack_client.api_call(
            'channels.info',
            channel=self.get_channel_id(channel_name)
        )
        if api_call.get('ok'):
            return api_call.get('channel').get('members')
        else:
            self.logger.error('The error %s was raised while '
                              'getting users!' % api_call.get('error'))
            return []

    def user_is_active(self, user_id):
        api_call = self.slack_client.api_call(
            'users.getPresence',
            user=user_id
        )
        if api_call.get('ok'):
            return api_call.get('presence')
        else:
            self.logger.error('The error %s was raised while '
                              'verifying if user is'
                              ' active!' % api_call.get('error'))
            return False

    def get_channel_id(self, channel_name):
        api_call = self.slack_client.api_call(
            'channels.list',
            exclude_archived=1
        )
        if api_call.get('ok'):
            for channel in api_call.get('channels'):
                if channel.get('name') == channel_name:
                    return channel.get('id')
        else:
            self.logger.error('The error %s was raised while '
                              'getting channel id!' % api_call.get('error'))

    def connect(self):
        return self.slack_client.rtm_connect()

    def read(self):
        return self.slack_lib.rtm_read()
