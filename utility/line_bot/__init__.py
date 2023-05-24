from .globals import linebot_manager

def initialize(app, echo: bool = False):

    channel_access_token = app.config['LINE_CHANNEL_ACCESS_TOKEN']
    channel_secret = app.config['LINE_CHANNEL_SECRET']
    linebot_manager.setup(channel_access_token, channel_secret)
    
    
    


