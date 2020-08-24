#/usr/bin/venv python3

#GET,POST,PUT VE DELETE METHODLARINI DESTEKLER.

from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API',
          )

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='The task details'),
    'surname': fields.String(required=True, description='The task details'),
    'age': fields.Integer(required=True, description='The task details')
})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:toor@172.17.0.3:5432/postgres"

db = SQLAlchemy(app)


class users_api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    age = db.Column(db.Integer())

    def __init__(self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo


DAO = TodoDAO()


#DAO.create({'name': 'Build an API','surname' : 'satleca', 'age' : 12})
#DAO.create({'name': 'asdsad','surname' : 'sdsd', 'age' : 15})
# DAO.create({'task': '?????'})
# DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''

    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''

        new_user = users_api(api.payload['name'], api.payload['surname'], api.payload['age'])
        db.session.add(new_user)
        db.create_all()
        db.session.commit()

        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        sil = users_api.query.filter_by(id=id).first()
        db.session.delete(sil)
        db.session.commit()
        return '', 204


    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''

        data = users_api.query.filter_by(id=id).first()
        data.name = api.payload['name'] 
        data.surname = api.payload['surname'] 
        data.age = api.payload['age']
        db.session.commit()
        
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=True)
