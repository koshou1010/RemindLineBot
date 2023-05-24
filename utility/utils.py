import datetime

def get_current_month():
    return str(datetime.datetime.now().year) + '-' +str(datetime.datetime.now().month)