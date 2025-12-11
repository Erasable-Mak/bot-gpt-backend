import connexion
from app.config import Config
from app.utils.db import db

def create_app():
    cnx_app = connexion.App(__name__, specification_dir="./swagger")
    cnx_app.add_api(
        "schema.yml",
        strict_validation=True,
        validate_responses=False,
        swagger_ui=True,
        base_path="/api"
    )
    app = cnx_app.app
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
