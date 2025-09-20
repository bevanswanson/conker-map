import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from models import db, Conker


app = Flask(__name__)
CORS(app)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://conker_user:conker_pass@db:5432/conker_db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/api/conkers", methods=["GET"])
def get_conkers():
    conkers = Conker.query.all()
    return jsonify([c.to_dict() for c in conkers])


@app.route("/api/conkers", methods=["POST"])
def add_conker():
    data = request.json
    new_conker = Conker(latitude=data['latitude'], longitude=data['longitude'], notes=data.get('notes', ''))
    db.session.add(new_conker)
    db.session.commit()
    return jsonify(new_conker.to_dict()), 201


if __name__ == "__main__":

    MAX_RETRIES = 10
    for attempt in range(MAX_RETRIES):
        try:
            with app.app_context():
                db.create_all()
            app.run(host='0.0.0.0', port=5000)
        except OperationalError:
            print(f"DB not ready, retry {attempt+1}/{MAX_RETRIES}")
            time.sleep(2)
    else:
        raise RuntimeError("Could not connect to DB after retries")
    