from flask import Blueprint
main = Blueprint('main', __name__)


@main.route('/', methods=['POST'])
def index():
    return {"status":True}, 200