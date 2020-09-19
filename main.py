from flask import Flask

# ===== Routing =====
from routes.main_routes import data

app = Flask(__name__)

# ===== Blueprints Registration =====
app.register_blueprint(data, url_prefix="/")