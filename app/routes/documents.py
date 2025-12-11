from flask import Blueprint, request, jsonify
from app import db
from app.models import Document, User
import uuid

bp = Blueprint('documents', __name__)

@bp.route('/documents', methods=['POST'])
def create_document():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    title = data.get('title')
    uri = data.get('uri')
    if not user_id or not title:
        return jsonify({"error": "user_id and title are required"}), 400
    if not User.query.get(user_id):
        return jsonify({"error": "User not found"}), 404
    doc = Document(id=str(uuid.uuid4()), user_id=user_id, title=title, uri=uri)
    db.session.add(doc)
    db.session.commit()
    return jsonify(doc.to_dict()), 201

@bp.route('/users/<user_id>/documents', methods=['GET'])
def list_documents(user_id):
    docs = Document.query.filter_by(user_id=user_id).order_by(Document.created_at.desc()).all()
    return jsonify([d.to_dict() for d in docs]), 200
