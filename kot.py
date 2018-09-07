from app import create_app, db
from app.database.models import User, Client, Quickpay

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Client': Client, 'Quickpay': Quickpay}