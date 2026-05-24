from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from app import db
# 1. Added Comment here!
from app.models import User, Post, Comment
# 2. Added CommentForm here!
from app.forms import PostForm, CommentForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)
    
    # Base query for all posts sorted by date
    query = Post.query.order_by(Post.date_posted.desc())
    
    # If the user typed something in the search bar, filter the results
    if search_query:
        query = query.join(User).filter(
            (Post.title.ilike(f'%{search_query}%')) | 
            (Post.content.ilike(f'%{search_query}%')) |
            (User.username.ilike(f'%{search_query}%'))
        )
    
    # Paginate our final filtered query (2 posts per page for easy testing)
    posts = query.paginate(page=page, per_page=2)
    
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
    return redirect(url_for('main.index'))

@main.route('/post/new', methods=['GET', 'POST'])
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

# 3. Upgraded Post Detail route to handle Comments!
@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    
    # If a user submits a comment
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to login to comment.', 'danger')
            return redirect(url_for('main.login'))
            
        # Create the comment and link it to the user and the post
        comment = Comment(content=form.content.data, author=current_user, parent_post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
        
    return render_template('post.html', post=post, form=form)

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

@main.route("/user/<string:username>")
def user_posts(username):
    # Find the user by their username, or return a 404 error if they don't exist
    user = User.query.filter_by(username=username).first_or_404()
    
    # Grab all posts written by this specific user, newest first
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    
    return render_template('user_posts.html', posts=posts, user=user)