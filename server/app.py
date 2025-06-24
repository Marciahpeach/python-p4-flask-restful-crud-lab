from flask import Flask
from server.config import db, migrate
from server.routes import plants_bp
from server.models import Plant
from flask_cors import CORS

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

CORS(app)
app.register_blueprint(plants_bp)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
