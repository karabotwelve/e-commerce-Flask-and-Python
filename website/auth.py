from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<p>logged in </p>"


@auth.route('/logout')
def logout():
    return "<p>logged out </p>"


@auth.route('/signup')
def sign_up():
    return "<p>signing out</p>"
