from flask import Flask, jsonify, render_template, redirect, request, url_for, session, flash
from itsdangerous import URLSafeTimedSerializer
# from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import db, Regions

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SECRET_KEY'] = ''
jwt = JWTManager(app)

db.init_app(app)

@app.route('/1462b4f3-6caa-4b86-8d5f-3ba880de8391', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if username == 'Luqmaan Abdallah' and password == 'Admin':
            access_token = create_access_token(identity=username)
            return jsonify({'message': 'success', 'access_token': access_token}), 200
    
        else:
            return jsonify({'error', 'Invalid username or password'})

@app.route('/regions', methods=['GET', 'POST'])
@jwt_required()
def get_regions():
    regions = Regions.query.all()

    result = [{'id': region.id, 'name': region.name, 'code': region.code} for region in regions]

    return jsonify(result)

@app.route('/add_region', methods=['GET','POST'])
@jwt_required()
def add_region():
    new_region_name = request.json['region']
    new_region_code = request.json['region-code']

    existing_region = Regions.query.filter_by(name=new_region_name).first()
    if existing_region:
        return jsonify({"error": "Region name already exists"}), 400

    existing_region_code = Regions.query.filter_by(code=new_region_code).first()
    if existing_region_code:
        return jsonify({"error": "Region code already exists"}), 400

    if new_region_name is not None:
        last_id = db.session.query(db.func.max(Regions.id)).scalar()
        new_id = 1 if last_id is None else last_id + 1

        new_region = Regions(id=new_id, name=new_region_name, code=new_region_code)
        db.session.add(new_region)
        db.session.commit()

        return jsonify({"success": "Data received successfully"}), 200
    else:
        return jsonify({"error": "Failed"}), 400
    

@app.route('/update_region', methods=['GET', 'POST'])
@jwt_required()
def update_region():
    region_to_update = request.json['region_to_update']
    selected_type = request.json['selected_type']
    value_to_replace = request.json['value_to_replace']

    if selected_type == 'region-name':
        update_region_name = Regions.query.filter_by(name=region_to_update).first()
        if update_region_name:
            update_region_name.name = value_to_replace
            db.session.commit()
            return jsonify({"success": "Region name updated successfully"}), 200
        else:
            return jsonify({"error": "Region not found"}), 404
    elif selected_type == 'region-code':
        update_region_code = Regions.query.filter_by(name=region_to_update).first()
        if update_region_code:
            update_region_code.code = value_to_replace
            db.session.commit()
            return jsonify({"success": "Region code updated successfully"}), 200
        else:
            return jsonify({"error": "Region not found"}), 404
    else:
        return jsonify({"error": "Invalid selected type"}), 400


@app.route('/delete_region', methods=['GET', 'POST'])
@jwt_required()
def delete_region():
    region_name = request.json['region']
    
    region_instance = Regions.query.filter_by(name=region_name).first()
    if region_instance is None:
        return jsonify({"error": "Region not found"}), 404
    
    else:
        db.session.delete(region_instance)
        db.session.commit()
    
        return jsonify({"success": f"Successfully deleted <strong>{region_name}</strong>"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
