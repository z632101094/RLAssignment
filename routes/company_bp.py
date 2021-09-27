from flask import Blueprint
from controllers.company_controller import create, delete, read, read_company_info

company_bp = Blueprint('company_bp', __name__)
company_bp.route('/create', methods=['POST'])(create)
company_bp.route('/delete', methods=['POST'])(delete)
company_bp.route('/read', methods=['GET'])(read)
company_bp.route('/read_company_info', methods=['GET'])(read_company_info)