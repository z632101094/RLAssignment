from flask import Blueprint
from controllers.user_controller import create, select, select_by_username, update, delete

user_bp = Blueprint('user_bp', __name__)
user_bp.route('/create', methods=['POST'])(create)
user_bp.route('/select', methods=['GET'])(select)
user_bp.route('/select_by_username', methods=['GET'])(select_by_username)
user_bp.route('/update', methods=['PUT'])(update)
user_bp.route('/delete', methods=['POST'])(delete)