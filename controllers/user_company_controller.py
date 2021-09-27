from flask import request, jsonify
from common.authorization import permission_required
from models import db
from models.user import Company, Permissions, User


@permission_required(Permissions.ADMIN)
def create():
    '''
    Create User_Company association
    :return:
    '''
    try:
        users_id = request.args.get('users_id')
        company_id = request.args.get('company_id')
        if not users_id or not company_id:
            ret_data = dict(code=1, ret_msg='Need users_id and company_id')
            return jsonify(ret_data)

        company = Company.query.get(company_id)
        user = User.query.get(users_id)
        if not company:
            ret_data = dict(code=1, ret_msg='Company does not exist')
            return jsonify(ret_data)
        if not user:
            ret_data = dict(code=1, ret_msg='User does not exist')
            return jsonify(ret_data)

        company.users.append(user)
        db.session.commit()
        ret_data = dict(code=0, ret_msg='Create Association Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Create Association Failed')
        return jsonify(ret_data)


@permission_required(Permissions.ADMIN)
def delete():
    '''
    Delete User_Company association
    :return:
    '''
    try:
        users_id = request.args.get('users_id')
        company_id = request.args.get('company_id')
        if not users_id or not company_id:
            ret_data = dict(code=1, ret_msg='Need users_id and company_id')
            return jsonify(ret_data)
        user = User.query.get(users_id)
        company = Company.query.get(company_id)
        if user not in company.users:
            ret_data = dict(code=1, ret_msg='Association does not exist')
            return jsonify(ret_data)
        company.users.remove(user)
        db.session.commit()
        ret_data = dict(code=0, ret_msg='Delete Association Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Delete Association Failed')
        return jsonify(ret_data)

@permission_required(Permissions.ADMIN)
def read():
    '''
    Read all User_Company association
    :return:
    '''
    try:
        result_list = []
        companys = Company.query.all()
        for company in companys:
            company_id = company.id
            users = company.users
            for user in users:
                user_id = user.id
                result_list.append({
                    'users_id': user_id,
                    'company_id': company_id
                })
        ret_data = dict(code=0, ret_msg='Read Association Successed', value = result_list)
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Read Association Failed')
        return jsonify(ret_data)

