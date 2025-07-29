# student_tracker.py

class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}

    def add_grade(self, subject, grade):
        if 0 <= grade <= 100:
            self.grades[subject] = grade
        else:
            raise ValueError("Grade must be between 0 and 100")

    def average_grade(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

    def get_info(self):
        return {
            "Name": self.name,
            "Roll Number": self.roll_number,
            "Grades": self.grades,
            "Average": self.average_grade()
        }


class StudentTracker:
    def __init__(self):
        self.students = {}

    def add_student(self, name, roll_number):
        if roll_number in self.students:
            raise ValueError("Roll number already exists.")
        self.students[roll_number] = Student(name, roll_number)

    def add_grade(self, roll_number, subject, grade):
        student = self.students.get(roll_number)
        if not student:
            raise ValueError("Student not found.")
        student.add_grade(subject, grade)

    def get_student_info(self, roll_number):
        student = self.students.get(roll_number)
        if student:
            return student.get_info()
        else:
            raise ValueError("Student not found.")

    def class_average_for_subject(self, subject):
        subject_scores = [s.grades[subject] for s in self.students.values() if subject in s.grades]
        return sum(subject_scores) / len(subject_scores) if subject_scores else 0

    def subject_topper(self, subject):
        topper = max(
            (s for s in self.students.values() if subject in s.grades),
            key=lambda s: s.grades[subject],
            default=None
        )
        return topper.get_info() if topper else None
