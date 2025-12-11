import os
import requests
import json
from app.config import Config
from typing import List, Dict, Any, Tuple

class LLMService:
    def __init__(self):
        self.config = Config()
        if self.config.LLM_PROVIDER == 'groq' and not self.config.GROQ_API_KEY and os.getenv("ALLOW_EMPTY_KEYS"):
            self.provider = 'stub'
        else:
            self.provider = self.config.LLM_PROVIDER

    def get_response(self, conversation_history: List[Dict[str, str]], mode: str = 'open_chat', context: str = None) -> Tuple[str, int]:
        """
        Get response from LLM based on conversation history
        Returns: (response_text, token_count)
        """
        if self.provider == 'groq':
            return self._get_groq_response(conversation_history, mode, context)
        elif self.provider == 'huggingface':
            return self._get_huggingface_response(conversation_history, mode, context)
        elif self.provider == 'stub':
            return "stub response", 0
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _get_groq_response(self, conversation_history: List[Dict[str, str]], mode: str, context: str) -> Tuple[str, int]:
        """Get response from Groq API"""
        if not self.config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable not set")

        # formatting messages for groq api endpoint
        messages = []

        # adding system message based on mode selection
        if mode == 'rag' and context:
            system_message = f"""
            You are a helpful assistant that answers questions based on the provided context.
            Use the context below to answer the user's question. If the context doesn't contain
            the information needed, say you don't have enough information to answer accurately.

            Context: {context}
            """
        else:
            system_message = "You are a helpful AI assistant."

        messages.append({"role": "system", "content": system_message})

        # conversation history addition
        for msg in conversation_history:
            messages.append({
                "role": "user" if msg['role'] == 'user' else "assistant",
                "content": msg['content']
            })

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config.GROQ_MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if not data or "choices" not in data or not data["choices"]:
                raise Exception(f"Unexpected response format from Groq API: {data}")

            assistant_reply = data["choices"][0]["message"].get("content", "") or ""
            token_usage = data.get("usage", {}).get("total_tokens", 0)
            return assistant_reply.strip(), token_usage

        except requests.HTTPError as http_err:
            body = http_err.response.text if http_err.response is not None else ""
            status = http_err.response.status_code if http_err.response is not None else "n/a"
            raise Exception(f"Groq API error {status}: {body}")
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")

    def _get_huggingface_response(self, conversation_history: List[Dict[str, str]], mode: str, context: str) -> Tuple[str, int]:
        """Get response from HuggingFace Inference API (stub implementation)"""
        # this is just a placeholder - here we can implement actual HuggingFace api call
        return "This is a simulated response from HuggingFace.", 50

    def simulate_rag_retrieval(self, query: str, document_ids: List[str]) -> str:
        """
        Simulate RAG retrieval for the case study.
        In a real implementation, this would query a vector database.
        For now, we'll return hardcoded context based on query.
        """
        # keyword based simulation
        query_lower = query.lower()

        if any(word in query_lower for word in ['python', 'code', 'programming']):
            return """Python is a high-level, interpreted programming language known for its readability and versatility. 
            It supports multiple programming paradigms including procedural, object-oriented, and functional programming. 
            Python's syntax emphasizes readability with its use of significant indentation."""

        elif any(word in query_lower for word in ['machine learning', 'ml', 'ai', 'model']):
            return """Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data. 
            It involves algorithms that improve automatically through experience. Common types include supervised learning, 
            unsupervised learning, and reinforcement learning."""

        elif any(word in query_lower for word in ['database', 'sql', 'query']):
            return """A database is an organized collection of data stored and accessed electronically. 
            SQL (Structured Query Language) is a standard language for managing and querying relational databases. 
            Common database systems include PostgreSQL, MySQL, SQLite, and MongoDB."""

        else:
            return """This is a general context for the conversation. The system is designed to provide helpful and accurate information 
            based on retrieved documents. In a real implementation, this context would come from relevant document chunks 
            retrieved using vector similarity search."""
