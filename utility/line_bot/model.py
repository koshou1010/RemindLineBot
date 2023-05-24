from linebot import LineBotApi, WebhookParser, WebhookHandler




class LineBotManager:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def setup(self, channel_access_token, channel_secret):
        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)
