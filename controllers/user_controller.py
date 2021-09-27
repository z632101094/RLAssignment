import hashlib

from flask import request, jsonify
from common.authorization import permission_required
from models import db
from models.user import User, Permissions, Role


@permission_required(Permissions.ADMIN)
def create():
    '''
    Create User
    :return:
    '''
    try:
        username = request.args.get('username')
        if User.query.filter_by(username=username).first():
            ret_data = dict(code=1, ret_msg='Username already existed')
            return jsonify(ret_data)
        password = request.args.get('password')
        role_id = request.args.get('role_id')
        if not Role.query.filter_by(id=role_id).first():
            ret_data = dict(code=1, ret_msg='Role does not exist')
            return jsonify(ret_data)
        account_permission = request.args.get('account_permission')
        if (type(account_permission) == str): #Check if the input paramater is a string
            account_permission = int(account_permission, 16)
        if account_permission == 10 or account_permission == 8 or account_permission == 2 or account_permission == 0:
            ret_data = dict(code=1, ret_msg='Account_Permission must be 0xa, 0x8, or 0x2')
            return jsonify(ret_data)
        new_user = User(username, password, role_id, account_permission)
        db.session.add(new_user)
        db.session.commit()

        ret_data = dict(code=0, ret_msg='Create User Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Create User Failed')
        return jsonify(ret_data)


@permission_required(Permissions.ADMIN)
def select():
    '''
    Select all User
    :return:
    '''
    try:
        users = User.query.all()
        result_list = []
        for user in users:
            role = Role.query.filter_by(id=user.role_id).first()
            result_list.append({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'role_id': user.role_id,
                'account_permission': user.account_permission,
                'role': {
                    'id': role.id,
                    'name': role.name,
                    'role_permission': role.role_permission
                }
            })
        ret_data = dict(code=0, ret_msg='Select all User Successed', value = result_list)
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Select all User Failed')
        return jsonify(ret_data)

@permission_required(Permissions.ADMIN)
def select_by_username():
    '''
    Select By Username
    :return:
    '''
    try:
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            ret_data = dict(code=1, ret_msg='Username does not exist')
            return jsonify(ret_data)
        role = Role.query.filter_by(id=user.role_id).first()
        user_result = {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'role_id': user.role_id,
            'account_permission': user.account_permission,
            'role': {
                'id': role.id,
                'name': role.name,
                'role_permission': role.role_permission
            }
        }
        ret_data = dict(code=0, ret_msg='Select User Successed', value = user_result)
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Select User Failed')
        return jsonify(ret_data)

@permission_required(Permissions.ADMIN)
def update():
    '''
    Update password, role_id, account_permission by username
    :return:
    '''
    try:
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            ret_data = dict(code=1, ret_msg='Username does not exist')
            return jsonify(ret_data)
        if request.args.get('password'):
            password = request.args.get('password')
            user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if request.args.get('role_id'):
            role_id = request.args.get('role_id')
            if not Role.query.filter_by(id=role_id).first():
                ret_data = dict(code=1, ret_msg='Role does not exist')
                return jsonify(ret_data)
            user.role_id = role_id
        if request.args.get('account_permission'):
            account_permission = request.args.get('account_permission')
            if (type(account_permission) == str): #Check if the input paramater is a string
                account_permission = int(account_permission, 16)
            if account_permission == 10 or account_permission == 8 or account_permission == 2 or account_permission == 0:
                ret_data = dict(code=1, ret_msg='Account_Permission must be 0xa, 0x8, or 0x2')
                return jsonify(ret_data)
            user.account_permission = account_permission
        db.session.commit()
        ret_data = dict(code=0, ret_msg='Update User Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Update User Failed')
        return jsonify(ret_data)


@permission_required(Permissions.ADMIN)
def delete():
    '''
    Delete By Username
    :return:
    '''
    try:
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            ret_data = dict(code=1, ret_msg='Username does not exist')
            return jsonify(ret_data)
        db.session.delete(user)
        db.session.commit()
        ret_data = dict(code=0, ret_msg='Delete User Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Delete User Failed')
        return jsonify(ret_data)