from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random():
    cafes = db.session.query(Cafe).all()
    random_cafe = choice(cafes)
    # print(random_cafe)
    return jsonify(id=random_cafe.id,
                   name=random_cafe.name,
                   map_url=random_cafe.map_url,
                   img_url=random_cafe.img_url,
                   location=random_cafe.location,
                   seats=random_cafe.seats,
                   has_toilet=random_cafe.has_toilet,
                   has_wifi=random_cafe.has_wifi,
                   has_sockets=random_cafe.has_sockets,
                   can_take_calls=random_cafe.can_take_calls,
                   coffee_price=random_cafe.coffee_price)


@app.route("/all")
def get_all_cafe():
    cafes = db.session.query(Cafe).all()
    all_cafes = []
    for cafe in cafes:
        new_entry = cafe.to_dict()
        all_cafes.append(new_entry)
    # print(all_cafes)

    return jsonify(cafes=all_cafes)


@app.route("/search")
def search():
    user_location = request.args.get("location_name")
    cafe = Cafe.query.filter_by(location=user_location).first()
    print(cafe)
    if cafe:
        return jsonify(cafe.to_dict())
    else:
        return jsonify(error='No Data Found')


## HTTP POST - Create Record

def str_to_bool(v):
    if v in ['True', ' true', 'T', 't', 'Yes', 'yes', 'y', '1']:
        return True
    else:
        return False


@app.route("/add", methods=["POST"])
def add_record():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=str_to_bool(request.form.get('has_toilet')),
        has_wifi=str_to_bool(request.form.get('has_wifi')),
        has_sockets=str_to_bool(request.form.get('has_sockets')),
        can_take_calls=str_to_bool(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price'))
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(accepted="Your data has been recieved successfully")


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_coffee_price(cafe_id):
    new_price = request.args.get('coffee_price')
    print(new_price)
    cafe_to_update = Cafe.query.get(cafe_id)
    if (cafe_to_update):
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"message": "Your Price Update change has been successfull"}), 200
    else:
        return jsonify(response={"error": "Resource not found"}), 404


## HTTP DELETE - Delete Records
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_record(cafe_id):
    api_key = request.args.get("api-key")
    print(api_key)
    cafe_to_delete = Cafe.query.get(cafe_id)
    if api_key == "sdfoisodif98jj93j" and cafe_to_delete:
        cafe_to_delete = Cafe.query.get(cafe_id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"message": "Your Cafe has been deleted successfully"}), 200
    else:
        return jsonify(response={"message": "Invalid Response"}), 403


if __name__ == '__main__':
    app.run(debug=True)
