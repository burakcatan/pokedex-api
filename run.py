from flask import Flask
from routes import app_bp
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.register_blueprint(app_bp)

if __name__ == '__main__':
    app.run()
