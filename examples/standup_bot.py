import logging
import os
from dotenv import load_dotenv
from slackclient import SlackClient

from slack_bot import SlackBot
from slack_bot import SlackClientWrapper

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
logging.basicConfig(format='[%(levelname)s] [%(name)s] - %(message)s',
                    level=logging.INFO)

slack_client = SlackClient(token=os.environ.get('SLACK_BOT_TOKEN'))
slack_wrapper = SlackClientWrapper(slack_lib=slack_client)
CHANNEL = os.environ.get('STANDUP_CHANNEL')


def validate_events(events):
    return events and len(events) > 0


def event_is_message(event):
    return event.get('type') == 'message'


def users_of_messages(events):
    users = []
    if validate_events(events):
        for event in events:
            if event_is_message(event):
                users.append(event.get('user'))
    return users


def wait_for_user_updates(user):
    events = slack_wrapper.read()
    while user.get('id') not in users_of_messages(events):
        events = slack_wrapper.read()


def send(message):
    slack_wrapper.post_message(
        channel=CHANNEL,
        message=message,
        as_user=True
    )


def standup():
    user_ids = slack_wrapper.get_channel_users(CHANNEL)
    user_ids.remove(slack_bot.id)
    send('Welcome to our standup!')
    for user_id in user_ids:
        user = slack_wrapper.get_user(user_id)
        get_user_update(user)
    send('That was all! Thanks for participate of this wonderful standup')


def get_user_update(user):
    questions = [
        '1. What did you do yesterday?',
        '2. What are you working on today?',
        '3. Do you have a blocker?'
    ]
    send('Hi %s is your turn!' % user.get('name'))
    for question in questions:
        send(question)
        wait_for_user_updates(user)
    send('Thanks! Good Luck!')


COMMAND_HANDLERS = {
    'standup': standup,
}


if __name__ == '__main__':
    slack_bot = SlackBot(
        bot_name=os.environ.get('BOT_NAME'),
        client=slack_wrapper,
        commands_handlers=COMMAND_HANDLERS
    )

    slack_bot.start()
