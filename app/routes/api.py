from flask import Blueprint, request, jsonify
from models import User, Company, TestResult
from main import db
import openai
import jwt
import bcrypt
from util.constants import boost
from datetime import datetime, timedelta
from PyPDF2 import PdfReader

api = Blueprint('api', __name__)

openai.api_key = db.app.config['OPENAI_API_KEY']

@api.route('/api/cv', methods=['POST'])
def extract_cv_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=boost+text,
            max_tokens=150,
            temperature=0.7
        )
        message = response.choices[0].text.strip()
        return jsonify({"response": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/api/companies', methods=['GET'])
def get_companies():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    characteristics = request.args.get('characteristics', '')
    companies = Company.query.filter(Company.name.contains(query),
                                     Company.characteristics.contains(characteristics)).all()
    return jsonify([{"id": c.id, "name": c.name, "characteristics": c.characteristics} for c in companies])

@api.route('/api/register', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed_password.decode('utf-8'), email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"})

@api.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)}, db.app.config['SECRET_KEY'])
    return jsonify({"token": token})

@api.route('/api/test', methods=['POST'])
def take_test():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        decoded_token = jwt.decode(token, db.app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    score = request.json.get('score', 0)
    test_result = TestResult(user_id=user_id, score=score)
    db.session.add(test_result)
    db.session.commit()

    return jsonify({"message": "Test completed", "score": score})

@api.route('/api/chat', methods=['POST'])
def chat_with_gpt():
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = openai.Completion.create(
            model="gpt-4-turbo",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        message = response.choices[0].text.strip()
        return jsonify({"response": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500