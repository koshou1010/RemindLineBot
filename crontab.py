##　　detection date to send https request to line bot send message
import datetime, requests, os, time
from utility.sql_alchemy.globals import sqlAlchemy_manager
from model.user import User
from model.user_save_progress import UserSaveProgress
from dotenv import load_dotenv
from utility.utils import get_current_month

res = load_dotenv("../app/config/.env")

LockName = 'cronjob_lock'

TEST_GROUP_ID = os.getenv('TEST_GROUP_ID')
GROUP_ID=os.getenv('GROUP_ID')


# def check_cpu_usage():
#     """
#     Check Currently CPU usage.
#     return true if usage greater than 35.5, which is not a good time to do job.
#     """
#     import psutil
#     cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
#     return cpu_usage > 35.5

class DataBaseInit:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    def __init__(self) -> None:
        self.mysql_connect()

    def mysql_connect(self):
        from utility.sql_alchemy import setup
        print(self.SQLALCHEMY_DATABASE_URI)
        setup(self.SQLALCHEMY_DATABASE_URI)
    
class CrontabController:
    def __init__(self):
        DataBaseInit()
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.mysql_engine_url = os.getenv('SQLALCHEMY_DATABASE_URI')
        
    def lock(self):
        print("Lock.")
        lock_file_name = os.path.join(self.file_path, LockName)
        lock = str(int(round(time.time() * 1000)))
        with open(lock_file_name, "w") as lock_file:
            print("Open Lock file.")
            lock_file.write(lock)
        print("Write Lock: {}".format(lock))

    def unlock(self):
        print("UnLock.")
        lock_file_name = os.path.join(self.file_path, LockName)
        if os.path.exists(lock_file_name):
            os.remove(lock_file_name)
            print("Remove Lock file.")


    
    def isLocked(self):
        print("Check Lock File Exist.")
        lock_file_name = os.path.join(self.file_path, LockName)
        islocked = True if os.path.exists(lock_file_name) else False
        print('{} exists :{}'.format(lock_file_name, islocked))
        return islocked
    
    def query_all_user(self):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(User).filter_by(
                valid_flag=True
            ).all()
        return query_result
    
    def create_save_progress_by_user_id(self, id: int):
        with sqlAlchemy_manager.Session() as session:
            insert_data = UserSaveProgress(
                user_id = id,
                valid_flag=True,
                create_user='koshou',
                update_user='koshou',
                month=get_current_month(),
                save_flag=False
            )
            session.add(insert_data)
            session.commit()
    
    def create_all_user_save_progress_by_month(self):
        res = self.query_all_user()
        for user in res:
            self.create_save_progress_by_user_id(user.id)
        pass

    def query_current_month_created(self):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(UserSaveProgress).filter_by(
                valid_flag=True,
                month=get_current_month()
            ).all()
        return query_result
    
    def query_user_by_user_id(self, id: int):
        with sqlAlchemy_manager.Session() as session:
            query_result = session.query(User).filter_by(
                valid_flag=True,
                id = id
            ).first()
        return query_result

    def excute_action(self):
        print(datetime.datetime.now())
        res = self.query_current_month_created()
        if res:
            for i in res:
                if not i.save_flag:
                    user = self.query_user_by_user_id(i.user_id)
                    data = {
                        "line_id":GROUP_ID,
                        "message":"今天是{}\r\n{}這個月存錢了沒?".format(datetime.datetime.now().date(), user.name)
                     }
                    response = requests.post(url='https://bd4a-1-164-82-18.ngrok-free.app/line/send', json=data)
        else:
            self.create_all_user_save_progress_by_month()
            if str(datetime.datetime.now().day) == "10":
                data = {
                    "line_id":GROUP_ID,
                    "message":"今天是{}\r\n各位這個月存錢了沒?".format(datetime.datetime.now().date())
                }
                response = requests.post(url='https://bd4a-1-164-82-18.ngrok-free.app/line/send', json=data)




if __name__ =="__main__":
    # if check_cpu_usage():
        # print("CPU usage is too high, pass migration now.")
    # else:
    print(os.getcwd())
    print(res)
    crontab_controller = CrontabController()
    if crontab_controller.isLocked():
        print("Currently Locked.")
    else:
        try:
            crontab_controller.lock()
            crontab_controller.excute_action()
        finally:
            crontab_controller.unlock()
    
