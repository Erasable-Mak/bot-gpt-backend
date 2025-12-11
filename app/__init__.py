from flask import Flask
from app.config import Config
from app.utils.db import db
from app.routes.conversations import bp as conversations_bp
from app.routes.users import bp as users_bp
from app.routes.documents import bp as documents_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # regestering blueprints here since connexion swagger/schema.yml not working
    app.register_blueprint(conversations_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(documents_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()
 
    return app
