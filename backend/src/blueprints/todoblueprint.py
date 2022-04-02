from flask import Blueprint, jsonify, abort, request
from flask_cors import cross_origin

import json

from pymongo.errors import WriteError

import src.controllers.todocontroller as controller

# instantiate the flask blueprint
todo_blueprint = Blueprint('todo_blueprint', __name__)

# create a new task
@todo_blueprint.route('/create', methods=['POST'])
@cross_origin()
def create():
    try:
        data = request.form.to_dict(flat=True)
        todo = controller.create_todo(data)
        return jsonify(todo), 200
    except WriteError as e:
        abort(400, 'Invalid input data')
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

# obtain one user by id (and optionally update him)
@todo_blueprint.route('/byid/<id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def get_todo(id):
    try:
        # get a specific todo
        if request.method == 'GET':
            todo = controller.get_todo(id)
            return jsonify(todo), 200
        # update the todo
        elif request.method == 'PUT':
            data = request.form.to_dict(flat=True)['data']
            data = json.loads(data.replace("'", "\""))

            todo = controller.update_todo(id, data)
            return jsonify(todo), 200
        elif request.method == 'DELETE':
            controller.delete_todo(id)
            return jsonify({'id': id}), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')