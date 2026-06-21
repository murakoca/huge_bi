from flask import Blueprint, render_template, request, redirect, url_for
from auth.models import create_user
from premium.capacity import CapacityMonitor

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    metrics = CapacityMonitor.get_metrics()
    return render_template('admin.html', metrics=metrics)

@admin_bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'viewer')
        create_user(username, password, role)
        return redirect(url_for('admin.users'))
    # Kullanıcı listesini veritabanından çekip göster
    return render_template('users.html', users=[])