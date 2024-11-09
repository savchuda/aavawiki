from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config 
from models import User, Company, Position, Tribe, TestResult
from routes import api 

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

app.register_blueprint(api)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
