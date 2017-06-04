import logging

from slackclient import SlackClient


class SlackClientWrapper:
    def __init__(self, slack_token, slack_lib=SlackClient):
        self.slack_client = slack_lib(slack_token)
        self.logger = logging.getLogger('SlackClientWrapper')

    def post_message(self, channel, message, as_user):
        """
        Send a message to a specific channel
        :param channel:
        :param message:
        :param as_user:
        :return: None
        """
        self.slack_client.api_call('chat.postMessage', channel=channel,
                                   text=message, as_user=as_user)

    def get_user(self, user_id):
        """
        Get Slack user
        :param user_id:
        :return: User
        :type: dict
        """
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

    def get_active_users(self, channel):
        """
        Get Slack active users of channel
        :param channel:
        :return: Users
        :type: list of dicts
        """
        user_ids = [
            user for user
            in self.get_channel_users(channel)
            if self.get_user_presence(user) == 'active'
            ]
        return [
            self.get_user(user_id)
            for user_id in user_ids
            ]

    def get_users(self):
        """
        Get Slack users
        :return: Users
        :type: list of dicts
        """
        self.logger.info('Getting users...')
        api_call = self.slack_client.api_call('users.list')
        if api_call.get('ok'):
            return api_call.get('members')
        else:
            self.logger.error('The error %s was raised while '
                              'getting users!' % api_call.get('error'))
            return []

    def get_channel_users(self, channel):
        """
        Get Slack Channel Users
        :param channel:
        :return: Users
        :type: list of dicts
        """
        self.logger.info('Getting users of channel %s...' % channel)
        api_call = self.slack_client.api_call(
            'channels.info',
            channel=self.get_channel_id(channel)
        )
        if api_call.get('ok'):
            return api_call.get('channel').get('members')
        else:
            self.logger.error('The error %s was raised while '
                              'getting users!' % api_call.get('error'))
            return []

    def get_user_presence(self, user_id):
        """
        Get Presence of user
        :param user_id:
        :return: Presence
        :type: str
        """
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
        """
        Get channel id
        :param channel_name:
        :return: Channel Id
        :type: str
        """
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
        return self.slack_client.rtm_read()
