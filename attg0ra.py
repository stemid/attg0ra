# Very standard JSON handler for the ToDo app.

from __future__ import print_function
from sys import stderr
from urllib import urlencode, unquote
from json import dumps, loads, JSONEncoder
from datetime import datetime
from bottle import route, run, request, default_app, response, debug
from Todo.Database import Database

db = Database()

# This is for encoding datetime objects to str since json cannot serialize
# datetime objects. Hooks into the default method of JSONEncoder class. 
class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return JSONEncoder.default(self, obj)

# List all the ToDo items or get one specific item.
@route('/', method='GET')
@route('/<date>', method='GET')
def list(date=None):
    response.content_type = 'application/json'

    if date is not None:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    # Make a list of items to respond with
    response_list = []
    try:
        for (edited, todo) in db:
            if date is not None and edited != date:
                continue
            todo_dict = loads(todo)
            todo_dict.update({
                'edited': edited
            })
            response_list.append(todo_dict)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    # Return 404 if the list is empty
    if not len(response_list):
        response.status = 404
        return { 'error': 'Not found' }

    # Return JSON data of the list, use the DateEncoder for datetime fields
    return dumps(response_list, cls = DateEncoder)

# Create a new item by POST.
@route('/', method='POST')
def create():
    response.content_type = 'application/json'

    print(response.body, file=stderr)
    created = datetime.now()
    try:
        jsonBody = loads(response.body)
        title = request.json.get('inputTitle', 'No title')
        todo = request.json.get('inputTodo', 'No content')
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    text = dumps({
        'created': str(created),
        'title': title,
        'text': todo
    })

    try:
        db.add_post(created, title, text)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    return { 'status': 'OK' }

# Delete an item.
@route('/<date>', method='DELETE')
def delete(date):
    response.content_type = 'application/json'

    edited = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    try:
        if db.is_post(edited) is False:
            response.status = 404
            return { 'error': 'Not found' }
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    try:
        db.delete_post(edited)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    return { 'status': 'Deleted' }

# Update an item.
@route('/<date>', method='UPDATE')
def update(date):
    response.content_type = 'application/json'

    edited = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    title = request.forms.get('inputTitle', 'No title')
    todo = request.forms.get('inputTodo', 'No content')

    try:
        if db.is_post(edited) is False:
            response.status = 404
            return { 'error': 'Not found' }
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    text = dumps({
        'created': str(edited),
        'title': title,
        'text': todo
    })

    try:
        db.update_post(edited, text)
    except Exception as e:
        response.status = 500
        return { 'error': str(e) }

    return { 'status': 'Updated' }

if __name__ == '__main__':
    run(host='0.0.0.0', port=8000)
    debug(True)
else:
    application = default_app()
