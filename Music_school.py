from flask import Flask
from views.classes import cla
from views.course import cou
from views.index import ind
from views.login import log
from views.users import use


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(cla)
app.register_blueprint(cou)
app.register_blueprint(ind)
app.register_blueprint(log)
app.register_blueprint(use)

if __name__ == '__main__':
    app.run(debug=True)
