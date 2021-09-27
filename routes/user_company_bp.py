from flask import Blueprint
from controllers.user_company_controller import create, delete, read

user_company_bp = Blueprint('user_company_bp', __name__)
user_company_bp.route('/create', methods=['POST'])(create)
user_company_bp.route('/delete', methods=['POST'])(delete)
user_company_bp.route('/read', methods=['GET'])(read)