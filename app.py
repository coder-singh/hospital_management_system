from extensions import create_app
from extensions import db


app = create_app('Prod')

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
