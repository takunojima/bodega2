from app import create_app, db
from app.models import User, Shift

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Shift': Shift}

if __name__ == '__main__':
    # Production
    app.run(host='0.0.0.0', port=80, debug=False)
    
    # Development - use port 5000 for local testing
    # app.run(host='0.0.0.0', port=5000, debug=True)
    
    # Production
    # app.run(host='0.0.0.0', port=443, ssl_context='/etc/letsencrypt/live/bodegashift.com/', debug=False) 