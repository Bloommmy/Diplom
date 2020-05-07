from app import add, db
from app.models import User, Form_all, Form_one, Form_two

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Form_all': Form_all, 'Form_one': Form_one, 'Form_two': Form_two}
