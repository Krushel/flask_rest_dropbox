# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from drop import *
from front import front

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(front, url_prefix='/front')


@app.route('/create', methods=['POST'])
def create():
    try:
        key = request.json['key']
        value = request.json['value']
        if not dropbox_path_exists(key):
            create_directory_at_path(key)
            try:
                upload_file(key, value)
                return jsonify({"success": True}), 200
            except Exception as e:
                return f'An error occured: {e}'
        else:
            return 'Pair with this key already exist, you can update it or delete'
    except Exception as e:
        return f'An error occured: {e}'

@app.route('/get/<string:key>', methods=['GET'])
def get(key):
    if key:
        try:
            if dropbox_path_exists(key):
                return read_file(key)
        except Exception as e:
            return f'An error occured: {e}'
    else:
        return 'No key'

@app.route('/update/<string:key>', methods=['POST', 'PUT'])
def update(key):
    value = request.json['value']
    if value:
        if key:
            if dropbox_path_exists(key):
                try:
                    delete_file_from_path(key)
                    create_directory_at_path(key)
                    upload_file(key, value)
                    return jsonify({"success": True}), 200
                except Exception as e:
                    return f'An error occured: {e}'
            else:
                return 'No such key'
        else:
            return 'No key'
    else:
        return 'No value'

@app.route('/delete/<string:key>', methods=['GET', 'DELETE'])
def delete(key):
    try:
        delete_file_from_path(key)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f'An error occured: {e}'

if __name__ == '__main__':
    app.run(threaded=True, debug=True)