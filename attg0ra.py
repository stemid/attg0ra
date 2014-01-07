# coding: utf-8
# JSON gränssnitt för Att Göra applikationen.

from __future__ import print_function
from sys import stderr
from urllib import urlencode, unquote
from json import dumps, loads, JSONEncoder
from datetime import datetime
from ConfigParser import ConfigParser
from bottle import route, run, request, default_app, response, debug
from Todo.Database import Database

# Global åtkomst till databasen
db = Database()

# Global konfiguration
config = ConfigParser()
config.read('attg0ra.cfg')

# Detta används för att serialisera datetime objekt till JSON. Biblioteket
# json klarar normalt sett inte av att hantera datetime objekt så de 
# omvandlas till strängar. 
class DateEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            #return str(obj)
            return obj.isoformat()
            #return obj.strftime('%Y-%m-%dT%H:%MZ')
        return JSONEncoder.default(self, obj)

# Detta är för att angular ska stödja CORS, alltså olika domäner för gränssnitt
# och API. 
@route('/', method='OPTIONS')
@route('/<date>', method='OPTIONS')
def options(date=None):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'GET, POST, UPDATE, DELETE, OPTIONS')
    response.add_header('Access-Control-Allow-Headers', 'X-Custom-Header')
    return 

# Lista alla inlägg eller hämta ett enskilt. 
@route('/', method='GET')
@route('/<date>', method='GET')
def list(date=None):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'GET')
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

# Skapa nya inlägg.
@route('/', method='POST')
def create():
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'POST')
    response.content_type = 'application/json'

    created = datetime.now()
    try:
        jsonBody = loads(request.body.getvalue())
        title = jsonBody.get('inputTitle', 'No title')
        todo = jsonBody.get('inputTodo', 'No content')
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

# Radera ett inlägg.
@route('/<date>', method='DELETE')
def delete(date):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'DELETE')
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

# Uppdatera ett inlägg
@route('/<date>', method='UPDATE')
def update(date):
    response.add_header('Access-Control-Allow-Origin', config.get('main', 'url'))
    response.add_header('Access-Control-Allow-Methods', 'UPDATE')
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
    run(
        host = config.get('api', 'host'), 
        port = config.get('api', 'port')
    )
    debug(config.get('api', 'debug'))
else:
    application = default_app()
