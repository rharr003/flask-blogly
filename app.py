from flask import Flask, redirect, request, render_template, session, url_for
from models import db, connect_db, User
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rharr003:Dissidia1!@127.0.0.1:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        f = request.form
        new_user = User(first_name=f['first_name'],last_name=f['last_name'], image_url=f.get('url'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/<int:user_id>', methods=['GET', 'POST'])
def details(user_id):
    selected_user = User.query.get(user_id)
    if request.method == 'POST':
        selected_user.first_name = request.form['first_name']
        selected_user.last_name = request.form['last_name']
        selected_user.image_url = request.form.get('url')
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('details.html', user=selected_user)

@app.route('/delete/<int:user_id>')
def delete(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:user_id>')
def edit(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)


app.run(debug=True)