from app import db
from datetime import datetime
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    conversations = db.relationship('Conversation', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Conversation(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # uuid format
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    mode = db.Column(db.String(20), default='open_chat')  # "open_chat" or "rag"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    document_ids = db.Column(db.Text, nullable=True)  # JSON array of document IDs if in RAG mode
    
    messages = db.relationship('Message', backref='conversation', lazy=True, order_by="Message.created_at")
    
    def to_dict(self, include_messages=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'mode': self.mode,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'document_ids': json.loads(self.document_ids) if self.document_ids else []
        }
        if include_messages:
            data['messages'] = [message.to_dict() for message in self.messages]
        return data

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "user" or "assistant" can be changed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tokens_used = db.Column(db.Integer, default=0)
    meta = db.Column(db.Text, nullable=True)  # json for additional metadata
    
    def to_dict(self):
        data = {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'content': self.content,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'tokens_used': self.tokens_used
        }
        if self.meta:
            data['metadata'] = json.loads(self.meta)
        return data

class Document(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    uri = db.Column(db.String(512), nullable=True)      # place where the file/chunks live/stored
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "uri": self.uri,
            "created_at": self.created_at.isoformat()
        }
