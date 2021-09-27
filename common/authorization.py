from functools import wraps
from flask import session, abort
from models.user import User, Role, Permissions


def check_authorization(current_user, permission_required):
    role = Role.query.filter_by(id=current_user.role_id).first()
    account_permission = current_user.account_permission
    role_permission = role.role_permission

    if permission_required == Permissions.COMPANY_INFO and role_permission == Permissions.ADMIN:
        #From the assignment requirement, it seems admin can not access COMPANY_INFO
        return False

    # Combine the role permission and account permission to get the actual permission
    actual_permission = role_permission | account_permission
    return permission_required & actual_permission == permission_required


def permission_required(permission_required):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                current_user = User.query.filter_by(id=session.get('user_id')).first()
                if not current_user or check_authorization(current_user, permission_required) == False:
                    abort(403)
                return f(*args, **kwargs)
            except:
                abort(403)
        return decorated_function
    return decorator