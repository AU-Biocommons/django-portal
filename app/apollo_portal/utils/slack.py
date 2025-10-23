"""Slack notifications for log handling."""

import os
import requests

SLACK_URL = "https://slack.com/api/chat.postMessage"


def post(message):
    """Post a message to Slack."""
    key = os.environ.get("SLACK_API_KEY")
    user_id = os.environ.get("SLACK_MENTION_USER_ID")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")
    hostname = os.environ.get("HOSTNAME", 'unknown server')

    if key is None:
        return

    mention_str = f'<@{user_id}> ' if user_id else ' '
    text = f'{mention_str}[{hostname}]\n{message}'

    requests.post(
        SLACK_URL,
        json={
            "text": text,
            "channel": channel_id,
        },
        headers={
            "Authorization": f'Bearer {key}',
        },
    )
