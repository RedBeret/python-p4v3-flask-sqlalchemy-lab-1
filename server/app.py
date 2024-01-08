# server/app.py
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import Earthquake, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


@app.route("/earthquakes/<int:id>")
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify(earthquake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    quakes = [quake.to_dict() for quake in earthquakes]
    return jsonify({"count": count, "quakes": quakes}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
