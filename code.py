from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from flask import render_template
from flask import redirect


#Create Flask application object 
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///wishlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#created an object for SQLAlchemy class with app as object
db=SQLAlchemy(app)


#In this class we will create the columns required
class Wishlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	wish = db.Column(db.Text)
	date = db.Column(db.Text)
	done=db.Column(db.Boolean, default=False)

	def __init__(self, wish,date):
		self.wish = wish
		self.date = date
		self.done = False

#To use database in URI
db.create_all()


@app.route('/')
def tasks_list():
    wishs = Wishlist.query.all()
    # print(wishs)
    return render_template('wishlist2.html', wishs=wishs)

@app.route('/wish', methods=['POST'])
def add_task():
	#get the content from wish column
    wish = request.form['wish']
    date = request.form['date']
    if not wish:
        return 'Error'
    val = Wishlist(wish,date)
    db.session.add(val)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    wish = Wishlist.query.get(task_id)
    if not wish:
        return redirect('/')
    db.session.delete(wish)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()


