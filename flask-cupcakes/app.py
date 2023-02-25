"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app_ctx = app.app_context()
app_ctx.push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)



@app.route('/')
def index_page():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes = cupcakes)
        

        
@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcak in particular"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    data = request.json

    new_cupcake = Cupcake(flavor=data['flavor'],rating=data['rating'], size=data['size'],image=data['image'] )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)



@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    data = request.json.get
    cupcake.flavor = data('flavor', cupcake.flavor)
    cupcake.size = data('size', cupcake.size)
    cupcake.rating = data('rating', cupcake.rating)
    cupcake.image = data('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")



