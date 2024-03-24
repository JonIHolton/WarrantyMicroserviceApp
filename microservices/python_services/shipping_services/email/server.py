from settings import config
from application import create_app
from flask_cors import CORS
from utils.helper import get_os
from threading import Thread


c = None
if get_os() == 'Windows':
    c=config['development']
elif get_os() == "Linux":
    c=config['production']

app = create_app(c)
CORS(app,origins='*')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
    