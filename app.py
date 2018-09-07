from app import create_app, db
from app.database.models import User, Client

app = create_app()

@app.shell_context_processor
def make_shell_context():
return {'db': db, 'User': User, 'Client': Client}

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)