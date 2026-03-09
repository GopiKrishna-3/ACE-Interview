from flask import Flask
from flask_cors import CORS
from app.routes import api_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("app.config.Config")
    
    app.register_blueprint(api_bp)

    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        with open("backend_error.log", "a") as f:
            f.write(traceback.format_exc() + "\n")
        return {"error": str(e)}, 500
    
    return app
