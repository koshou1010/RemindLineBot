from linebot.models import MessageEvent, TextMessage, TextSendMessage
# from model.line_link import LineLink
from model.user import User
from model.user_save_progress import UserSaveProgress
from utility.sql_alchemy.globals import sqlAlchemy_manager
from utility.line_bot.globals import linebot_manager
from sqlalchemy import func
import time, datetime

class LineModel:
    

    def __init__(self) -> None:
        self.link_task_status = {
            "sign_up" : {"flag" : 0, "time":None}
        }
    
    def link_task_status_reset(self):
        self.link_task_status = {
            "agree_terms" : {"flag" : 0, "time":None},
            "name_check" : {"flag" : 0, "time":None}
        }
    
    def create_user(self, line_id, signup_name,start_signup=False, end_signup=False):
        with sqlAlchemy_manager.Session() as session:
            insert_data = User(
                line_id = line_id,
                name=signup_name,
                valid_flag=True,
                create_user='koshou',
                update_user='koshou',
                start_signup=start_signup,
                end_signup= end_signup
            )
            session.add(insert_data)
            session.commit()
    
    def update_user_save_progress_by_user_id(self, id: int, current_month: str):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(UserSaveProgress).filter(
                UserSaveProgress.user_id==id,
                UserSaveProgress.valid_flag==True,
                UserSaveProgress.month==current_month
            ).update({'save_flag' : True})
            session.commit()
        return query_result
    
    # def query_user_exist(self, user_name) -> bool:
    #     with sqlAlchemy_manager.Session() as session:
    #         query_result = session.query(User.id, User.uuid, User.line_id, User.name).filter_by(name=user_name).first()
    #         session.commit()
    #     return query_result
    
    def query_user_by_line_id(self, line_id: str):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(User).filter_by(
                line_id=line_id,
                valid_flag=True
            ).first()
        return query_result
    
    
    def update_user_name(self, line_id: str, name: str):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(User).filter(
                User.line_id==line_id,
                User.valid_flag==True
            ).update({'name' : name})
            session.commit()
        return query_result
    

    
    def update_user_end_signup(self, line_id: str):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(User).filter(
                User.line_id==line_id,
                User.valid_flag==True
            ).update({'end_signup' : True})
            session.commit()
        return query_result
    
    # def create_line_link(self, line_id: str):
    #     self.link_task_status_reset()
    #     with sqlAlchemy_manager.Session() as session:
    #         insert_data = LineLink(
    #             line_id = line_id,
    #             link_task_status=self.link_task_status
    #         )
    #         session.add(insert_data)
    #         session.commit()
        
    # def update_link_task_status_and_link_uuid(self, primary_key: int, status: str, uuid: int):
    #     with sqlAlchemy_manager.Session() as session:
    #         target_flag_key = '$.{}.{}'.format(status,'flag')
    #         target_flag_time = '$.{}.{}'.format(status,'time')
    #         session.query(LineLink).filter_by(id=primary_key, valid_flag=True).update({
    #             LineLink.link_task_status: func.json_set(LineLink.link_task_status, target_flag_key, True)})
    #         session.query(LineLink).filter_by(id=primary_key, valid_flag=True).update({
    #             LineLink.link_task_status: func.json_set(LineLink.link_task_status, target_flag_time, int(time.time())),
    #             LineLink.uuid: uuid,
    #             LineLink.linked_time: datetime.datetime.now()
    #         })
    #         session.commit()
    
            
    def send_message(self, line_id: str,message: str):
        linebot_manager.line_bot_api.push_message(line_id, TextSendMessage(text=message))
        pass