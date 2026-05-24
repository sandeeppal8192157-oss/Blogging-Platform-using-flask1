from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from app import db
from app.models import User, Post
from app.forms import PostForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Fetch all posts from the database, newest first
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # Send the posts to the new index.html template
    return render_template('index.html', posts=posts)

@main.route('/register', methods=['GET', 'POST'])
def register():
    # If they are already logged in, send them home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    # If they clicked the "Sign Up" button
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email is already in the database
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered! Please login.', 'danger')
            return redirect(url_for('main.register'))
            
        # Scramble the password for security before saving
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists AND the scrambled passwords match
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    # When the user clicks the "Post" button and the form is valid
    if form.validate_on_submit():
        # Create a new post attached to the current logged-in user
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('create_post.html', form=form)
@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('create_post.html', form=form)
@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # SECURITY: If the logged-in user is NOT the author, kick them out!
    if post.author != current_user:
        abort(403) 
        
    form = PostForm()
    if form.validate_on_submit():
        # Save the new edited text to the database
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        # Pre-fill the form with the old text so they don't have to start from scratch
        form.title.data = post.title
        form.content.data = post.content
        
    # We can reuse the exact same HTML form we used to create posts!
    return render_template('create_post.html', form=form)