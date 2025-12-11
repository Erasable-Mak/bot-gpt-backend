import uuid
from datetime import datetime
from app.models import Conversation, Message, Document
from app import db
from .llm_service import LLMService
import json

class ConversationService:
    def __init__(self):
        self.llm_service = LLMService()
    
    def create_conversation(self, user_id: int, first_message: str, mode: str = 'open_chat', document_ids: list = None) -> dict:
        """Create a new conversation with the first message"""
        conversation_id = str(uuid.uuid4())
        document_ids_json = json.dumps(document_ids) if document_ids else None
        
        # conversation creation
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            mode=mode,
            document_ids=document_ids_json,
            title=first_message[:50] + "..." if len(first_message) > 50 else first_message
        )
        db.session.add(conversation)
        
        # user message addition check
        user_message = Message(
            conversation_id=conversation_id,
            content=first_message,
            role='user'
        )
        db.session.add(user_message)
        
        # assistant response
        context = None
        if mode == 'rag' and document_ids:
            docs = Document.query.filter(Document.id.in_(document_ids)).all()
            if len(docs) != len(document_ids):
                missing = set(document_ids) - {d.id for d in docs}
                raise ValueError(f"Documents not found: {', '.join(missing)}")
            context = self.llm_service.simulate_rag_retrieval(first_message, document_ids)
        
        conversation_history = [{"role": "user", "content": first_message}]
        assistant_reply, tokens_used = self.llm_service.get_response(conversation_history, mode, context)
        
        # assistant message addition
        assistant_message = Message(
            conversation_id=conversation_id,
            content=assistant_reply,
            role='assistant',
            tokens_used=tokens_used
        )
        db.session.add(assistant_message)
        
        db.session.commit()
        
        return conversation.to_dict(include_messages=True)
    
    def add_message_to_conversation(self, conversation_id: str, user_message: str) -> dict:
        """Add a new message to an existing conversation"""
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        
        # user message addition
        user_msg = Message(
            conversation_id=conversation_id,
            content=user_message,
            role='user'
        )
        db.session.add(user_msg)
        
        # conversation history fetch
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
        conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages]
        
        # context if RAG mode fetch
        context = None
        if conversation.mode == 'rag' and conversation.document_ids:
            document_ids = json.loads(conversation.document_ids)
            context = self.llm_service.simulate_rag_retrieval(user_message, document_ids)
        
        # assistant response fetch
        assistant_reply, tokens_used = self.llm_service.get_response(conversation_history, conversation.mode, context)
        
        # assistant message addition
        assistant_msg = Message(
            conversation_id=conversation_id,
            content=assistant_reply,
            role='assistant',
            tokens_used=tokens_used
        )
        db.session.add(assistant_msg)
    
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
        
        return conversation.to_dict(include_messages=True)
    
    def get_user_conversations(self, user_id: int) -> list:
        """Get all conversations for a user"""
        conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()
        return [conv.to_dict() for conv in conversations]

    def get_conversation_by_id(self, conversation_id: str) -> dict:
        """Get a specific conversation with all messages"""
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found")
        return conversation.to_dict(include_messages=True)

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and all its messages"""
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return False

        # try delete all messages first and then delete conversation
        Message.query.filter_by(conversation_id=conversation_id).delete()

        db.session.delete(conversation)
        db.session.commit()
        return True
