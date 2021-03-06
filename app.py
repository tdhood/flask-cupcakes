"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake, DEFAULT_IMAGE

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

db.create_all()

@app.get("/")
def root():
    """render homepage"""

    return render_template("homepage.html")


@app.get("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Create dessert from POST data and return it.

    Returns JSON {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    # image = request.json.get("image") #get value at image or returns default
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    """
     data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    """
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_a_cupcake(cupcake_id):
    """Return JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)

    if request.json["image"]:
        cupcake.image = request.json["image"]
    else:
        cupcake.image = DEFAULT_IMAGE
    
    """
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.size = data.get('size', cupcake.size)

    if "image" in data:
        cupcake.image = data['image'] or DEFAULT_IMAGE

    """

    # cupcake.image = request.json.get("image", cupcake.image)
    # check for empty string for image key

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)

@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_a_cupcake(cupcake_id):
    """delete cupcake from database
    
    Returns JSON {deleted: 'cupcake_id'}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    # {deleted: [cupcake-id]}

    return jsonify(deleted=cupcake_id)
