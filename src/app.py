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

# GENERA EL SITIOWEB CON LOS ENDPOINTS
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#ENDPOINT GET PARA TODOS LOS MIEMBROS
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    if not members:
        return jsonify({"msg": "The request body is empty"}), 404
    return jsonify(members), 200

    
#ENDPOINT GET PARA UN MIEMBRO ESPECIFICO
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    return jsonify(member), 200


#ENDPOINT POST PARA AGREGAR UN MIEMBRO
@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.json
    if not request_body:
        return jsonify({'msg': 'Bad Request'}), 400
    member = jackson_family.add_member(request_body)
    return jsonify(member), 200



#ENDPOINT DELETE PARA BORRAR UN MIEMBRO
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member = jackson_family.get_member(id)
 
    if member:
        jackson_family.delete_member(id)
        return jsonify({"done": True, "message": f"Member deleted successfully: {member}"}), 200
    else:
        return jsonify({"done": False, "error": "Member not found"}), 404




#SE ENVIA A PUERTO 3000
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)



