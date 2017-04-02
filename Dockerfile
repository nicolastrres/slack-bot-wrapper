FROM python:3.5


ENV APP_HOME /slack-bot
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt        $APP_HOME
RUN pip install -r requirements.txt

COPY slack_bot            $APP_HOME/slack_bot/
COPY tests                $APP_HOME/tests/