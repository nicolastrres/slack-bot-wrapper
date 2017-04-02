# slack-bot-wrapper

Allows to create Slack bots and add features to them very easily.
It uses the [python-slackclient](https://github.com/slackapi/python-slackclient) and creates a wrapper for it.


# Example

```python
import os
from slackclient import SlackClient
from slack_bot import SlackClientWrapper
from slack_bot import SlackBot

def bye():
    slack_wrapper.post_message(
        channel='some-channel',
        message='Bye! :slightly_smiling_face:',
        as_user=True
    )

def hello():
    slack_wrapper.post_message(
        channel='some-channel',
        message='Hello! :smile:',
        as_user=True
    )


# Commands that the bot understand, it is a dict with the name of the command as key and the 
# function that will be executed as value.
COMMAND_HANDLERS = {
    'hello': hello,
    'bye': bye
}


if __name__ == '__main__':
    # First import the python-slackclient and instantiate it.
    slack_client = SlackClient(token=os.environ.get('SLACK_BOT_TOKEN'))

    # Instantiate the SlackClientWrapper with the slack client.
    slack_wrapper = SlackClientWrapper(slack_lib=slack_client)

    # Instantiate the slack bot sending the bot name, client wrapper and the commands
    slack_bot = SlackBot(
        bot_name='bot-name',
        client=slack_wrapper,
        commands_handlers=COMMAND_HANDLERS
    )

    # Start the slack bot, it allows the bot to start reading messages and interact with the users
    slack_bot.start()
```

For a more complex examples take a look to the examples folder.
