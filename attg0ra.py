# Very standard JSON handler for the ToDo app.

from urllib import urlencode, unquote
from json import dumps, loads, JSONEncoder
from datetime import datetime
from bottle import route, run, request, default_app
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
    from bottle import response
    response.content_type = 'application/json'

    if date is not None:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

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

    if not len(response_list):
        response.status = 404
        return { 'error': 'Not found' }

    return dumps(response_list, cls = DateEncoder)

# Create a new item by POST.
@route('/', method='POST')
def create():
    from bottle import response
    response.content_type = 'application/json'

    created = datetime.now()
    title = request.forms.get('inputTitle', 'No title')
    todo = request.forms.get('inputTodo', 'No content')

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
    from bottle import response
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
    from bottle import response
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
    run(host='localhost', port=8000, debug=True)
else:
    application = default_app()
