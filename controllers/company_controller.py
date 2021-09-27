import hashlib

from flask import request, jsonify
from common.authorization import permission_required
from models import db
from models.user import Company, Permissions


@permission_required(Permissions.ADMIN)
def create():
    '''
    Create Company
    :return:
    '''
    try:
        id = request.args.get('id')
        if Company.query.get(id):
            ret_data = dict(code=1, ret_msg='Company already existed')
            return jsonify(ret_data)
        new_company = Company(id)
        db.session.add(new_company)
        db.session.commit()
        ret_data = dict(code=0, ret_msg='Create Company Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Create User Failed')
        return jsonify(ret_data)

@permission_required(Permissions.ADMIN)
def delete():
    '''
    Delete by id
    :return:
    '''
    try:
        id = request.args.get('id')
        company = Company.query.get(id)
        if not company:
            ret_data = dict(code=1, ret_msg='Company does not exist')
            return jsonify(ret_data)
        db.session.delete(company)
        db.session.commit()
        ret_data = dict(code=0, ret_msg='Delete Company Successed')
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Delete Company Failed')
        return jsonify(ret_data)

@permission_required(Permissions.COMPANY_LISTS)
def read():
    '''
    Read all Companys
    :return:
    '''
    try:
        companys = Company.query.all()
        result_list = []
        for company in companys:
            result_list.append({'id': company.id})
        ret_data = dict(code=0, ret_msg='Read Company List Successed', value = result_list)
        return jsonify(ret_data)
    except:
        ret_data = dict(code=1, ret_msg='Read Company List Failed')
        return jsonify(ret_data)

@permission_required(Permissions.COMPANY_INFO)
def read_company_info():
    '''
    Read Company Info
    :return:
    '''
    #try:
    id = request.args.get('id')
    company = Company.query.get(id)
    if not company:
        ret_data = dict(code=1, ret_msg='Company does not exist')
        return jsonify(ret_data)
    company_info = hashlib.sha256(str(id).encode('utf-8')).hexdigest()
    result = {
        'id': id,
        'company_info': company_info
    }

    ret_data = dict(code=0, ret_msg='Read Company Info Successed', value = result)
    return jsonify(ret_data)
    #except:
    #    ret_data = dict(code=1, ret_msg='Read Company Info Failed')
    #    return jsonify(ret_data)

