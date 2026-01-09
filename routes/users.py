from flask import Blueprint
from flask import redirect, url_for, flash, request, render_template
from models import db, AppPost, User
from flask_login import current_user, login_required

dashboard_bp = Blueprint("dashboard" , __name__)
admin_bp = Blueprint("admin" , __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    posts = AppPost.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', posts=posts)

@admin_bp.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin': return redirect(url_for('index'))
    pending = AppPost.query.filter_by(status='pending').all()
    reported = AppPost.query.filter(AppPost.reports > 0).order_by(AppPost.reports.desc()).all()
    users = User.query.all()
    return render_template('admin.html', pending=pending, reported=reported, users=users)

@admin_bp.route('/admin/approve/<int:id>')
@login_required
def approve_post(id):
    if current_user.role != 'admin': return "403", 403
    post = db.session.get(AppPost, id)
    if post:
        post.status = 'approved'
        db.session.commit()
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/user/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin': return "403", 403
    user = db.session.get(User, id)
    if user and user.role != 'admin':
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.admin_panel'))
