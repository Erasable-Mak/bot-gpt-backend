from flask import Blueprint, request, jsonify
from app.models import User
from app import db

bp = Blueprint('users', __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data or 'username' not in data:
        return jsonify({'error': 'Missing required field: username'}), 400

    username = data['username']
    email = data.get('email')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    # creation of user and above checking if user exist before this
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200
