from flask import Flask, send_file, request, jsonify
from models import db, Student
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_prefixed_env()

db.init_app(app)
migration = Migrate(app, db)

@app.before_request
def beforerequest():
    authed = False
    if request.path.startswith("/uploads") and authed == False:
        return "Prouted route. you need to be logged in", 403


@app.route("/")
def home():
    return send_file("./static/index.html")

@app.route("/uploads/<string:filename>")
def uploads(filename):
    return send_file(f"./uploads/{filename}")

@app.route('/students')
def students():
    
    students = Student.query.all()
    students_data = [student.to_dict() for student in students]

    return students_data, 200

@app.route('/students/<int:id>')
def students_id(id):
    
    student = Student.query.filter(Student.id==id).first()

    return student.to_dict(), 

@app.route('/students')
def create_students():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return {"error": "Name and email are required."}, 400

    if Student.query.filter_by(email=email).first():
        return {"error": "Email already exists."}, 409

    new_student = Student(name=name, email=email)
    db.session.add(new_student)
    db.session.commit()

    return new_student.to_dict(), 201




# MISSING MODULE psycopg2

