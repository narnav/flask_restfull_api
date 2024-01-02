import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100))

@app.route('/')
def hello():
    return {'test':"working"}

@app.route('/get_students_data', methods=['GET'])
def get_students_data():
    my_students = Student.query.all()
    print(my_students)
    students_data = []
    for student in my_students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'email': student.email,
        }
        students_data.append(student_data)
    return jsonify(students_data)

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['email']
        new_student = Student(name=name, email=email)
        db.session.add(new_student)
        db.session.commit()
        # students.append({"name": name, "email": email})
        # print(students)
    return {'add':"done"}

# Route to delete a student by ID
# del_data
@app.route('/del_data/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    print(student_id)
    if student:
        print(student)
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': f'Student with ID {student_id} deleted successfully'})
    else:
        return jsonify({'message': 'Student not found'}), 404

# Route to update a student's data by ID
@app.route('/upd_data/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)

    if student:
        data = request.get_json()
        student.name = data.get('name', student.name)
        student.email = data.get('email', student.email)

        db.session.commit()
        return jsonify({'message': f'Student with ID {student_id} updated successfully'})
    else:
        return jsonify({'message': 'Student not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
