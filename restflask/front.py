from flask import Blueprint, request, jsonify
from drop import *

front = Blueprint('front', __name__)

@front.route('/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            key = request.form['key']
            value = request.files['value']
            if not dropbox_path_exists(key):
                create_directory_at_path(key)
                try:
                    upload_file(path=key, file=value)
                    return jsonify({"success": True}), 200
                except Exception as e:
                    return f'An error occured: {e}'
            else:
                return 'Pair with this key already exist, you can update it or delete'
        except Exception as e:
            return f'An error occured: {e}'
    else:
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=text name=key>
              <input type=file name=value>
              <input type=submit value=Upload>
            </form>
            '''
