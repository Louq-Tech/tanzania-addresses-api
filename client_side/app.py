import requests
from flask import Flask, jsonify, render_template, redirect, request, url_for, session, flash, make_response
from itsdangerous import URLSafeTimedSerializer
import requests.cookies
# from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)

app.config['SECRET_KEY'] = 'example'
app.debug = True

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        data = {'username': username, 'password': password}

        session['username'] = username

        response = requests.post('http://127.0.0.1:5000/1462b4f3-6caa-4b86-8d5f-3ba880de8391', json=data, headers={'Content-Type': 'application/json'})

        if 'success' in response.json().get('message'):
            access_token = response.json().get('access_token')
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('access_token', access_token)
            return resp
        
        else:
            return redirect(url_for('/'))
        
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = session.get('username')
    return render_template('dashboard.html', user=user)

@app.route('/get_regions', methods=['GET','POST'])
def get_regions():
    return redirect(url_for('regions'))

@app.route('/regions', methods=['GET', 'POST'])
def regions():
    access_token = request.cookies.get('access_token')
    response = requests.get('http://127.0.0.1:5000/regions', headers={'Authorization': f'Bearer {access_token}'})
    regions = response.json()

    return render_template('regions_page.html', regions=regions)

@app.route('/add_region', methods=['GET','POST'])
def add_region():
    new_region_name = request.form['add-region']
    new_region_code = request.form['add-region-code']

    data = {'region': new_region_name, 'region-code': new_region_code}

    access_token = request.cookies.get('access_token')
    new_region = requests.post('http://127.0.0.1:5000/add_region', json=data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'})
    message = new_region.json().get('error')

    if 'success' in new_region.json():
        flash(f'Successfully added <strong>{new_region_name}</strong> with code name <strong>{new_region_code}</strong>', 'success')
        return redirect(url_for('dashboard'))
    
    else:
        flash(f'There was a problem adding <strong>{new_region_name}</strong> region : REASON <strong>{message}</strong>', 'error')

        return redirect(url_for('dashboard'))
    
@app.route('/update_region', methods=['GET', 'POST'])
def update_region():
    region_to_update = request.form['region-to-update']
    selected_type = request.form['selected-type']
    value_to_replace = request.form['value-to-replace']

    data = {
        'selected_type': selected_type,
        'region_to_update': region_to_update,
        'value_to_replace': value_to_replace
    }

    access_token = request.cookies.get('access_token')
    response = requests.post('http://127.0.0.1:5000/update_region', json=data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'})
    message = response.json().get('error')
    
    if 'success' in response.json():
        flash(f'Successfully updated <strong>{selected_type}</strong> for <strong>{region_to_update}</strong> with <strong>{value_to_replace}</strong>', 'success')
        return redirect(url_for('dashboard'))
    
    else:
        flash(f'There was a problem updating <strong>{region_to_update}</strong> region: REASON <strong>{message}</strong>', 'error')
        return redirect(url_for('dashboard'))

@app.route('/delete_region', methods=['GET', 'POST'])
def delete_region():
    region_name = request.form['region-name']
    
    access_token = request.cookies.get('access_token')
    deleted_region = requests.post('http://127.0.0.1:5000/delete_region', json={'region': region_name}, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'})
    message = deleted_region.json().get('error')

    if 'success' in deleted_region.json():
        flash(f"Successfully deleted <strong>{region_name}</strong>", "success")
        return redirect(url_for('dashboard'))
    
    else:
        flash(f'There was a problem deleting <strong>{region_name}</strong> region: REASON <strong>{message}</strong>', 'error')
        return redirect(url_for('dashboard'))
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()

    response = make_response(redirect(url_for('login')))
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)

    response.headers['Clear-Site-Data'] = '"cache", "cookies", "storage"'

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
