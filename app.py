from flask import Flask, redirect, request, render_template, session, url_for
from models import db, connect_db, User, Post
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
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:user_id>')
def edit(user_id):
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/addpost/<int:user_id>', methods=['GET', 'POST'])
def add_post(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/{user.id}')
    return render_template('addpost.html', user=user)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/edit/post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(f'/posts/{post.id}')
    return render_template('editpost.html', post=post)
app.run(debug=True)