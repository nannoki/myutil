
"""
Slackに一方的に投稿
"""

# from slackbot.bot import Bot
from slacker import Slacker
from settings import post2slack_private as setting


class Post2Slack:

    def __init__(self):
        self.__slacker = Slacker(setting.API_TOKEN)


    def post_message_to_channel(self, *, channel_name=setting.DEFAULT_CHANNEL, message, username,
                                icon_emoji=setting.DEFAULT_ICON, attachments=None):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        channel_name    : チャンネル名。 #は不要。
        message         : 投稿するテキストメッセージ
        username        : Slackに表示する投稿者名。何でも良い。
        icon_emoji      : 投稿者のアイコン絵文字。両端をコロンで囲む。　例） :emoji:
        attachments     : 添付
        """
        self.__slacker.chat.post_message(channel_name, message,
                                         icon_emoji=icon_emoji,
                                         username=username,
                                         unfurl_links=True,
                                         attachments=attachments
                                         )


if __name__ == "__main__":


    slack = Post2Slack()

    msg = 'pythonからの投稿テスト'
    attachments = {}

    # 絵文字名は両端をコロンで囲む
    slack.post_message_to_channel(message=msg,
                                  username='テスト中',
                                  attachments=attachments)
    print('メッセージをslackに投稿しました : [{}]'.format(msg))
