import os
from flask import Flask, jsonify
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["STORAGE_FILE"] = os.getenv("STORAGE_FILE", "./data/transacoes.json")

    from src.api.routes import bp as api_bp
    app.register_blueprint(api_bp)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
