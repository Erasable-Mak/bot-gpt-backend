from flask import Blueprint, request, jsonify
from app.models import User
from app.services.conversation_service import ConversationService

bp = Blueprint('conversations', __name__)
conversation_service = ConversationService()

@bp.route('/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation with the first message"""
    data = request.get_json()

    if not data or 'user_id' not in data or 'message' not in data:
        return jsonify({'error': 'Missing required fields: user_id and message'}), 400

    user_id = data['user_id']
    message = data['message']
    mode = data.get('mode', 'open_chat')  # mode selection 'open_chat' or 'rag'
    document_ids = data.get('document_ids', [])

    # verifying user exist or not (most cases can query on top and do getone)
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': f'User with ID {user_id} not found'}), 404

    try:
        conversation = conversation_service.create_conversation(
            user_id=user_id,
            first_message=message,
            mode=mode,
            document_ids=document_ids
        )
        return jsonify(conversation), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/conversations/<conversation_id>/messages', methods=['POST'])
def add_message(conversation_id):
    """Add a new message to an existing conversation"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing required field: message'}), 400
    
    message = data['message']
    
    try:
        conversation = conversation_service.add_message_to_conversation(
            conversation_id=conversation_id,
            user_message=message
        )
        return jsonify(conversation), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<user_id>/conversations', methods=['GET'])
def get_user_conversations(user_id):
    """Get all conversations for a user"""
    try:
        conversations = conversation_service.get_user_conversations(int(user_id))
        return jsonify(conversations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get a specific conversation with all messages"""
    try:
        conversation = conversation_service.get_conversation_by_id(conversation_id)
        return jsonify(conversation), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation and all its messages"""
    try:
        success = conversation_service.delete_conversation(conversation_id)
        if success:
            return jsonify({'message': 'Conversation deleted successfully'}), 200
        else:
            return jsonify({'error': 'Conversation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
