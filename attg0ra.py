from urllib import urlencode, unquote
from json import dumps, loads, JSONEncoder
from datetime import datetime
from bottle import route, run, request
from Todo.Database import Database

db = Database()

# This is for encoding datetime objects to str since json cannot serialize
# datetime objects. 
class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return JSONEncoder.default(self, obj)

@route('/', method='GET')
def list():
    from bottle import response
    response.content_type = 'application/json'

    response_list = []
    for (edited, todo) in db:
        todo_dict = loads(todo)
        todo_dict.update({
            'edited': edited
        })
        response_list.append(todo_dict)

    if not len(response_list):
        response.status_code = 404
        return { 'error': 'Not found' }

    return dumps(response_list, cls = DateEncoder)

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
        response.status_code = 500
        return { 'error': str(e) }

    return { 'status': 'OK' }

@route('/<date>', method='DELETE')
def delete(date):
    from bottle import response
    response.content_type = 'application/json'

    edited = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    if db.is_post(edited) is False:
        response.status_code = 404
        return { 'error': 'Not found' }

    try:
        db.delete_post(edited)
    except Exception as e:
        response.status_code = 500
        return { 'error': str(e) }

    return { 'status': 'OK' }

@route('/<date>', method='UPDATE')
def update(date):
    from bottle import response
    response.content_type = 'application/json'

    edited = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    title = request.forms.get('inputTitle', 'No title')
    todo = request.forms.get('inputTodo', 'No content')

    if db.is_post(edited) is False:
        response.status_code = 404
        return { 'error': 'Not found' }

    text = dumps({
        'created': str(edited),
        'title': title,
        'text': todo
    })

    try:
        db.update_post(edited, text)
    except Exception as e:
        response.status_code = 500
        return { 'error': str(e) }

    return { 'status': 'OK' }

if __name__ == '__main__':
    run(host='localhost', port=8000, debug=True)
