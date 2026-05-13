from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "<h1>Blog Home Page</h1><p>Week 1 structure is complete!</p>"