import hashlib
import json
from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from passlib.handlers.bcrypt import bcrypt_sha256

from common.authorization import permission_required
from models import db
from models.user import User, Permissions, Role
from routes import user_company_bp
from routes.company_bp import company_bp
from routes.user_bp import user_bp
from routes.user_company_bp import user_company_bp

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(company_bp, url_prefix='/company')
app.register_blueprint(user_company_bp, url_prefix='/user_company')



@app.route('/')
@app.route('/home')
def home():
    return '<h1>home</h1>'
    #password = 'admin'
    #return hashlib.sha256(password.encode('utf-8')).hexdigest()


@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
    Login
    :return:
    '''
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        if username and password:
            current_user = User.query.filter_by(username=username).first()
            encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if current_user and current_user.password == encrypted_password:
                user_id = current_user.id
                session['user_id'] = user_id
                ret_data = dict(code=0, ret_msg="login success")
            else:
                ret_data = dict(code=1, ret_msg='username or password is wrong')
        else:
            ret_data = dict(code=1, ret_msg='please input user_name or password')
    else:
        ret_data = dict(code=0, ret_msg='please login')

    return jsonify(ret_data)



if __name__ == '__main__':
    app.run()
