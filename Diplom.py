from app import add, db
from app.models import User, Faculty, Department, Degree, Direction, Profile, groupStud, Form_all, Form_one, Form_two

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Form_all': Form_all, 'Faculty': Faculty, 'Department': Department, 'Degree': Degree, 'Direction': Direction, 'Profile': Profile, 'groupStud': groupStud, 'Form_one': Form_one, 'Form_two': Form_two}
