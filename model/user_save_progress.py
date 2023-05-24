from utility.sql_alchemy.base import BaseModel, Column, types, ForeignKey
from utility.sql_alchemy.globals import Base, sqlAlchemy_manager
from utility.sql_alchemy.func import generate_uuid


class UserSaveProgress(BaseModel, Base):
    __tablename__ = 'user_save_progress'
    
    id = Column(types.Integer, primary_key=True, autoincrement=True)
    user_id =Column(types.Integer, ForeignKey('user.id'), nullable=False)
    month = Column(types.String(255), nullable=False)
    save_flag = Column(types.Boolean, nullable=False, default=False)


    @classmethod
    def find_by_id(cls, id):
        with sqlAlchemy_manager.Session() as session:
            query = session.query(cls).filter_by(Id=id, ValidFlag=True)
            result = next(iter(query or []), None)
        return result

    @classmethod
    def find_by_id_token(cls, id_token):
        with sqlAlchemy_manager.Session() as session:
            query = session.query(cls).filter_by(IdToken=id_token, ValidFlag=True)
            result = next(iter(query or []), None)
        return result

    @classmethod
    def find_by_code(cls, code):
        with sqlAlchemy_manager.Session() as session:
            query = session.query(cls).filter_by(Code=code, ValidFlag=True)
            result = next(iter(query or []), None)
        return result

    @classmethod
    def find_all_list(cls):
        with sqlAlchemy_manager.Session() as session:
            result = session.query(cls).filter_by(ValidFlag=True).all()
        return result
