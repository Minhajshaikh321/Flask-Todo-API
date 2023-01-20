from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


# instantiate flask app
app=Flask(__name__)
# set configs
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#instantiate db object
db = SQLAlchemy(app)
# create marshmallow
ma=Marshmallow(app)
# create database table
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return self.id

#create todolist schema
class TodoListSchema(ma.Schema):
    class Meta:
        fields=('id','name','description','completed','date_created')

#create insatnce of schemas
todolist_schema = TodoListSchema(many=False)
todolists_schema = TodoListSchema(many= True)

#create todos route
@app.route("/todolist", methods=["POST"])
def add_todo():
        # print("inside function")
    try:
        name=request.json['name']
        description=request.json['description']
        new_todo=TodoList(name=name,description=description)
        # print(new_todo)
        db.session.add(new_todo)
        db.session.commit()

        return todolist_schema.jsonify(new_todo)

    except Exception as e:
        return jsonify({"Error":"inavlid request."})

@app.route("/todolist/", methods=["GET"])
def get_todos():
    todos = TodoList.query.all()
    result_set = todolists_schema.dump(todos)
    return jsonify(result_set)

@app.route("/todolist/<int:id>", methods=["GET"])
def get_todo(id):
    todo=TodoList.query.get_or_404(int(id))
    return todolist_schema.jsonify(todo)


# update todo
@app.route("/todolist/<int:id>", methods=["PUT"])
def update_todo(id):

    todo=TodoList.query.get_or_404(int(id))

    name=request.json['name']
    description=request.json['description']
    completed=request.json['completed']

    todo.name=name
    todo.description=description
    todo.completd=completed

    db.session.commit()

    return todolist_schema.jsonify(todo)


# delete todo by id
@app.route("/todolist/<int:id>", methods=["DELETE"])
def delete_todo(id):
    todo=TodoList.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"Success":"Todo deleted"})



#create database
with app.app_context():
    db.create_all()
# @app.route("/create")
# def database():
#     db.create_all()
#     return ({"msg":"Function created"})

if __name__ == '__main__':
    app.run(debug=True)