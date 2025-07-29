from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    grades = db.relationship('Grade', backref='student', cascade="all, delete", lazy=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add Student route
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        if Student.query.filter_by(roll_number=roll).first():
            flash("Roll number already exists.", "danger")
        else:
            student = Student(name=name, roll_number=roll)
            db.session.add(student)
            db.session.commit()
            flash("Student added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Add Grade route
@app.route('/add_grade', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        roll = request.form['roll']
        subject = request.form['subject']
        grade_val = int(request.form['grade'])

        student = Student.query.filter_by(roll_number=roll).first()
        if not student:
            flash("Student not found.", "danger")
        else:
            grade = Grade(subject=subject, grade=grade_val, student=student)
            db.session.add(grade)
            db.session.commit()
            flash("Grade added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_grade.html')

# View Student Info
@app.route('/student_info', methods=['GET', 'POST'])
def student_info():
    student_data = None
    if request.method == 'POST':
        roll = request.form['roll']
        student = Student.query.filter_by(roll_number=roll).first()
        if student:
            grades = {g.subject: g.grade for g in student.grades}
            average = round(sum(grades.values()) / len(grades), 2) if grades else 0
            student_data = {
                "Name": student.name,
                "Roll Number": student.roll_number,
                "Grades": grades,
                "Average": average
            }
        else:
            flash("Student not found.", "danger")
    return render_template('student_info.html', student=student_data)

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
