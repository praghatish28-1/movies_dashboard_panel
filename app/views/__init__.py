# app/views/__init__.py
from .auth_views import bp as auth_bp
from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint('index', __name__,)

@bp.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('auth.login'))