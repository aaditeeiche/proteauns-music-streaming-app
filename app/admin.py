from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin dashboard
@bp.route('/dashboard')
def dashboard():
    # Fetch and display app statistics
    # Fetch flagged songs
    return render_template('admin/dashboard.html')

# Flagged songs
@bp.route('/flagged_songs')
def flagged_songs():
    # Fetch and display flagged songs
    return render_template('admin/flagged_songs.html')

# Blacklist/Whitelist creators
@bp.route('/blacklist_whitelist_creators')
def blacklist_whitelist_creators():
    # Fetch and display creators and provide an interface for blacklist/whitelist
    return render_template('admin/blacklist_whitelist_creators.html')
