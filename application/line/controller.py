from flask import Blueprint, request,send_from_directory
from utility.line_bot.globals import linebot_manager
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json, time, re
from .model import LineModel
import datetime, requests
from utility.utils import get_current_month

main = Blueprint('line', __name__)
line_model = LineModel()

GROUP_ID = "Cf83130be1ac1e1f259a6f8418493bf71"
test='C520e4409adaaebd2188f4288ec04dabd'

@main.route('/call_back', methods=['POST'])
def call_back():
    body = json.loads(request.get_data(as_text=True))
    client_msg = body['events'][0]['message']['text']
    line_id = body['events'][0]['source']['userId']
    # print(body)
    # print(client_msg)
    # print(line_id)
    

    

    if "Reminder" in client_msg:
        regex = re.match("Reminder \D*", client_msg)
        if regex:
            msg_split_len = regex.group().split(' ')
            res = line_model.query_user_by_line_id(line_id)
            if len(msg_split_len) == 2:
                real_msg = msg_split_len[-1]
                if real_msg == "存了":
                    if res:
                        line_model.update_user_save_progress_by_user_id(res.id, get_current_month())
                        line_model.send_message(GROUP_ID, "收到")
                    else:
                       line_model.send_message(GROUP_ID, "尚未註冊") 
                
            elif len(msg_split_len) == 3:
                if msg_split_len[1] == "註冊":
                    if res:
                        line_model.send_message(GROUP_ID, "你已經註冊過了")
                    else:
                        signup_name = msg_split_len[2]
                        line_model.create_user(line_id, signup_name, start_signup=True, end_signup=True)
                        line_model.send_message(GROUP_ID, "註冊成功")
            
            

        
        
    # line_link_obj = line_model.query_line_obj(line_id)
    # if not line_link_obj:
    #     if client_msg == "agree":
    #         line_model.link_task_status['agree_terms'] = {"flag" : True, "time":time.time()}
    #         line_model.create_line_link(line_id)
    #         line_model.send_message(line_id, "隱私條款同意成功")
    #         line_model.send_message(line_id, "開始綁定beatinfo 帳號")
    #         line_model.send_message(line_id, "請輸入名稱")
    #     else:
    #         line_model.send_message(line_id, "請同意隱私條款, 請輸入 agree ")
    #     return {"status":True,"message":"success"} 
    # if not line_link_obj.link_task_status['name_check']['flag']:
    #     user = line_model.query_user_exist(client_msg)
    #     if user:
    #         line_model.send_message(line_id, "Hi, {}".format(user.name))
    #         line_model.send_message(line_id, "開始綁定")
    #         line_model.update_link_task_status_and_link_uuid(line_link_obj.id, "name_check", user.uuid)
    #         line_model.send_message(line_id, "綁定成功")
    #     else:
    #         line_model.send_message(line_id, "未找到名稱")
    #     return {"status":True,"message":"success"}

    return {"status":True,"message":"success"},200


@main.route('/line/send', methods=['POST'])
def send_message():
    data = request.get_json()
    print(data)
    line_model.send_message(data['line_id'], data['message'])
    return {
        "status":True,
        "message":"success"
    }