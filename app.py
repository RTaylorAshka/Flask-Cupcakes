"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sweetsDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/')
def get_homepage():

    cupcakes = Cupcake.query.all()
    return render_template('home.html', cupcakes = cupcakes)

@app.route('/api/cupcakes', methods = ['GET'])
def get_all_cupcakes():

    all_cupcakes = [cupcake.serialize for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes', methods = ['POST'])
def create_new_cupcake():

    new_cupcake = Cupcake(flavor = request.json['flavor'], size = request.json['size'], rating = request.json['rating'])

    if 'image' in request.json:
        new_cupcake.image = request.json['image']

    db.session.add(new_cupcake)
    db.session.commit()
    json_res = jsonify(cupcake = new_cupcake.serialize)

    return (json_res, 201)

@app.route('/api/cupcakes/<int:id>', methods = ['GET'])
def get_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake = cupcake.serialize)

@app.route('/api/cupcakes/<int:id>', methods = ['PATCH'])
def update_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake = cupcake.serialize)

@app.route('/api/cupcakes/<int:id>', methods = ['DELETE'])
def delete_cupcake(id):

    Cupcake.query.filter_by(id = id).delete()
    db.session.commit()

    deletion_msg = {
        "message" : "cupcake deleted"
    }

    return jsonify(deletion_msg)

