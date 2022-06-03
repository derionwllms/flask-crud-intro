# crash course provided by freecodecamp.org via youtube https://www.youtube.com/watch?v=Z1RJmh_OqeA
from urllib import request
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # tells the app where the database is located
db = SQLAlchemy(app)                                        # initializes the databse with the settings defined in preious line

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/', methods=['POST', 'GET'])            # creates the routing for GET/POST methods
def index():
    if request.method == 'POST':                    # if POST(create) request is made, take contents of new task and adds it to the Todo object 
        task_content = request.form['content']      # takes the contents of the 'content' form in 'index.html' and saves it to a variable
        new_task = Todo(content=task_content)       # creates a new Todo iteration to be submitted into the database

        try:
            db.session.add(new_task)                # tries to commit the changes to the database then return us to thee index url
            db.session.commit()
            return redirect('/')
        except: 
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # if no request method is called then show the latest list ordered from oldest
        return render_template("index.html", tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)      # attempts to get task by ID otherwise it sends a 404 

    try:
        db.session.delete(task_to_delete)           # if the task ID was retrived then delete it from the database
        db.session.commit()
        return redirect('/')

    except:
        return "There was a problem deleting"

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)