from app import app, db
from app.models import User, Form, Faculty, Department

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Form': Form, 'Faculty': Faculty, 'Department': Department}
