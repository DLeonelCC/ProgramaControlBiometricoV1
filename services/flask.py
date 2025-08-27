from flask import Flask
from routes.home import home_bp
from routes.status import status_bp
from routes.sync import sync_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(sync_bp)
    return app

def run_flask(app, port=5000):
    app.run(port=port, debug=False, use_reloader=False)