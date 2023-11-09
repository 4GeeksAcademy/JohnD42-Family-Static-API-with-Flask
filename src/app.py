"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    
    try:
        members = jackson_family.get_all_members()
    except:
        return jsonify({"msg": "The server encountered an error."}), 500

    if members != None: 

        return jsonify(members), 200
    else:
        return jsonify({"msg": "That family doesn't exist."}), 404

@app.route('/member/<int:id>', methods=['GET'])
def handle_get_member(id):

    # this is how you can use the Family datastructure by calling its methods
    try:
        member = jackson_family.get_member(id)
    except:
        return jsonify({"msg": "The server encountered an error."}), 500

    if member != None: 

        return jsonify(member), 200
    else:
        return jsonify({"msg": "Invalid family member ID."}), 404

@app.route('/member', methods=['POST'])
def handle_add_member():
    member = request.get_json()
    member_id = member["id"]
    if "id" in member:
        duplicate_member_id = jackson_family.get_member(member_id)
        if duplicate_member_id is not None:
            return jsonify({"msg": "New  family member must not use an existing ID."}), 400
    if "lucky_numbers" in member and "age" in member and "first_name" in member:
        try:
            jackson_family.add_member(member)
        except:
            return jsonify({"msg": "The server encountered an error."}), 500

        return jsonify(), 200
    else:
        return jsonify({"msg": "Family members must have a first_name, age, and lucky_numbers."}), 400

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):

    # this is how you can use the Family datastructure by calling its methods
    if jackson_family.get_member(id) is None:
        return jsonify({"msg": "No such member ID."}), 404

    try:
        jackson_family.delete_member(id)
    except:
        return jsonify({"msg": "Member not successfully deleted. Is the ID correct?"}), 500

    if jackson_family.get_member(id) is None:
        return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
