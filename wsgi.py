import os
from application import create_app
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv("./config/.env")

app = create_app(mode=os.getenv('MODE'))
CORS(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
